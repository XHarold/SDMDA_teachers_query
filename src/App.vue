<template >
  <div class="app">
    <header class="header">
     
      <!-- 头部导航栏 -->
       <div id="navv">
    <ul>
      <li v-for="(item, index) in navItems" :key="index">
        <a :href="item.href" @click="handleClick(item.id)" @mouseover="handleMouseOver(item.id)" @mouseout="handleMouseOut(item.id)">{{ item.text }}</a>
        <div :class="`slider${item.id}`" :style="item.style"></div>
      </li>
    </ul>

  </div>
  <!-- 音乐 -->
  <div>
    
    <audio ref="audio" src="/bgm.mp3" loop autoplay></audio>
       <div class="slider-block">
         <el-slider v-model="volume" :min="0" :max="100" @change="setVolume"></el-slider>
       </div>
     </div>

      <div class="bg">
        <!-- 电子科技的图片 -->
        <el-col :span="24">
            <!-- <img src="@/assets/topbjtp.jpg" alt="" class="background-image"> -->
        </el-col>
      </div>
        
        <!-- 老师轮播图 -->
        <div class="teacher-carousel">
        <el-row>
          <el-col :span="24">
            <el-carousel :interval="2000" arrow="always" type="card" height="350px" 
            :trigger="manual"  :limit="3" >
              <el-carousel-item v-for="pic in pics" :key="pic.id">
                 <el-card body-style="text-align: center;">
                  <img :src="pic.src" alt="Teacher Photo">
                </el-card>
              </el-carousel-item>
            </el-carousel>
          </el-col>
        </el-row>
        </div>
        
        <!-- 筛选框 -->
         <!-- 标题 -->
        
         <h1 >教 师 查 询 / Teacher Search</h1>
         <img src="@/assets/uestc_header.png" alt="" class=""  style="display: block; margin-left: auto; margin-right: auto;">

        <div>
          <el-row class="filter-box">
            <el-col :span="24">
              <el-form inline>
                <el-form-item label="学院" >
                  <el-select v-model="filters.school" placeholder="全部" @change="applyFilters" style="width: 200px;">
                    <el-option label="全部" value=""/>
                    <el-option v-for="school in uniqueSchools" :key="school" :label="school" :value="school"/>
                  </el-select>
                </el-form-item>
                <el-form-item label="职称">
                  <el-select v-model="filters.title" placeholder="全部" @change="applyFilters" style="width: 100px;">
                    <el-option label="全部" value=""/>
                    <el-option v-for="title in uniqueTitles" :key="title" :label="title" :value="title"/>
                  </el-select>
                </el-form-item>
                <el-form-item label="姓氏字母">
                  <el-select v-model="filters.initial" placeholder="全部" @change="applyFilters" style="width: 80px;">
                    <el-option label="全部" value=""/>
                    <el-option v-for="initial in uniqueInitials" :key="initial" :label="initial" :value="initial"/>
                  </el-select>
                </el-form-item>
                <!-- 名字查老师 -->
                <el-form-item width="500px" label-position="top">
                  <el-form inline>
                    <el-input v-model="filters.name" placeholder="请输入姓名"  style="width: 300px;"></el-input>
                    <el-button type="primary" @click="applyFilters">查询</el-button>
                  </el-form>
                </el-form-item>
             
      </el-form>
      </el-col>
    </el-row>
    </div>

    <!-- 教师卡片 -->
    <div class="teacher-cards">
     <el-row :gutter="20">
        <el-col :span="4" v-for="teacher in paginatedTeachers" :key="teacher.id">
          <el-card body-style="padding: 0; cursor: pointer;" class="teacher-card">
            <a :href="teacher.url" target="_blank">
              <img :src="teacher.picUrl" class="teacher-photo" alt="teacher photo" />
            </a>
            <div style="padding: 14px;">
              <div class="teacher-info">{{ teacher.name }}</div>
              <div class="teacher-title">{{ teacher.prorank }}</div>
            </div>
          </el-card>
        </el-col>
         <template v-if="!paginatedTeachers || paginatedTeachers.length === 0">
      <div class="no-teachers">查无此老师</div>
    </template>
      </el-row>
      <!-- 分页 -->
      <div class="pagination">
      <el-pagination
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    :current-page="currentPage"
    :page-size="pageSize"
    layout="total, sizes, prev, pager, next, jumper"
    :total="filteredTeachers.length">
  </el-pagination>
</div>
    </div>



   <div class="waveWrapper">
     <div class="waveWrapperInner bgTop">
       <div class="wave waveTop" style="background-image:url('/wave-top.png') ;"></div>
     </div>
     <div class="waveWrapperInner bgMiddle">
       <div class="wave waveMiddle" style="background-image: url('/wave-mid.png');"></div>
     </div>
     <div class="waveWrapperInner bgBottom">
       <div class="wave waveBottom" style="background-image: url('/wave-bot.png');"></div>
     </div>
   </div>


</header>

</div>
</template>



<script>
import axios from 'axios';
import { ref, computed } from 'vue';
import pinyin from 'pinyin';


export default {
  
  setup() {

      
    const tableData = ref([]);
    
    const filters = ref({
       name: '',
      school: '',
      title: '',
      initial: '',
    });
    const currentPage = ref(1); //设置默认为第1页
    const pageSize = ref(12); // 设置每页显示的卡片数量为12

    //筛选职称的所有选项，计算所有独特的职称，学院同理
    const uniqueTitles = computed(() => {
      const titlesSet = new Set();
      tableData.value.forEach(teacher => {
        titlesSet.add(teacher.prorank);
      });
      return Array.from(titlesSet);
    });

     //学院同理
     const uniqueSchools = computed(() => {
      const schoolsSet = new Set();
      tableData.value.forEach(teacher => {
        schoolsSet.add(teacher.school);
      });
      return Array.from(schoolsSet);
    });

    // 计算所有独特的拼音首字母
    const uniqueInitials = computed(() => {
      const initialsSet = new Set();
      tableData.value.forEach(teacher => {
      const surname = teacher.name; 
    try {
      const pinyinResult = pinyin(surname, {
        style: pinyin.STYLE_FIRST_LETTER // 只获取拼音的首字母
      });
      if (Array.isArray(pinyinResult) && typeof pinyinResult[0][0] === 'string'
    && pinyinResult[0][0].length === 1)
     {
        const firstLetter = pinyinResult[0][0].toUpperCase(); // 转换为大写
        initialsSet.add(firstLetter); // 添加到集合
      } else { 
        initialsSet.add(pinyinResult[0][0][0])
        
      }
    } catch (error) {
      console.error('Error processing pinyin for teacher:', teacher, error);
    }
  });
  return Array.from(initialsSet).sort(); // 排序
});

    // 设置筛选条件
    const filteredTeachers = computed(() => {
  return tableData.value.filter(teacher => {
    try {
      const nameMatch = !filters.value.name || teacher.name.includes(filters.value.name);
      const pinyinResult = pinyin(teacher.name[0], {
        style: pinyin.STYLE_FIRST_LETTER // 只获取拼音的首字母
      });
      if (Array.isArray(pinyinResult) && typeof pinyinResult[0][0] === 'string') {
        const firstLetter = pinyinResult[0][0].toUpperCase(); // 转换为大写
        return (filters.value.title === '' || teacher.prorank === filters.value.title) &&
               (filters.value.initial === '' || firstLetter === filters.value.initial)&& (filters.value.school === '' || teacher.school === filters.value.school) &&
               nameMatch ;
      } else {
        console.error('pinyinResult[0][0][0] is not a string:', pinyinResult[0][0]);
        return false;
      }
    } catch (error) {
      console.error('Error processing pinyin for teacher:', teacher, error);
      return false;
    }
  });
});

     const paginatedTeachers = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value;
      const end = start + pageSize.value;
      return filteredTeachers.value.slice(start, end);
    });

    const applyFilters = () => {
       currentPage.value = 1; //重置分页到第一页
      // 手动触发计算属性更新
    };
    // 从后端获取数据
    const fetchTeachers = async () => {
      const response = await axios.get("http://127.0.0.1:8000/all_teachers");
      tableData.value = response.data.teachers;
    };

    const handleSizeChange = (newSize) => {
      pageSize.value = newSize;
    };

    //分页功能，更新数据
    const handleCurrentChange = (newPage) => {
      currentPage.value = newPage;
    };

    return {

       
      tableData,
      filteredTeachers,
      filters,
      currentPage,
      pageSize,
      uniqueSchools,
      uniqueTitles,
      uniqueInitials,
      paginatedTeachers,
      fetchTeachers,
      applyFilters,
      handleSizeChange,
      handleCurrentChange
    };
  },
  data() {
    return {
       pics: [
        { id: 1, src: '/byj/byj01.jpg'},
        { id: 2, src: '/byj/byj02.jpg'},
        { id: 3, src: '/byj/byj03.jpg'},
        { id: 4, src: '/byj/byj04.jpg'},
        { id: 5, src: '/byj/byj05.jpg'},
        { id: 6, src: '/byj/byj06.jpg'},
        { id: 7, src: '/byj/byj07.jpg'},
        { id: 8, src: '/byj/byj08.jpg'},
      ],

       navItems: [
        { id: 1, text: '首页', href: '#', style: { display: 'none' } },
        { id: 2, text: '教师课程', href: 'https://search.bilibili.com/all?keyword=%E7%94%B5%E5%AD%90%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6&from_source=webtop_search&spm_id_from=333.1007&search_source=5', style: { display: 'none' } },
        { id: 3, text: '研究生教育', href: 'https://gr.uestc.edu.cn/', style: { display: 'none' } },
        { id: 4, text: '本科生教育', href: 'https://www.jwc.uestc.edu.cn/Index.action', style: { display: 'none' } },
        { id: 5, text: '科研平台', href: 'https://www.rd.uestc.edu.cn/kypt.htm', style: { display: 'none' } },
      ],

      volume: 100, // 音乐音量
      isMusicPlaying: true, // 音乐是否正在播放的布尔值
    }},
  // 组件加载时立即获取数据
  mounted() {
    this.fetchTeachers();
    this.toggleMusic();
     
  },
   methods: {
    toggleMusic() {
      this.isMusicPlaying = !this.isMusicPlaying;
      this.isMusicPlaying ? this.$refs.audio.play() : this.$refs.audio.pause();
    },
    setVolume() {
      this.$refs.audio.volume = this.volume/100;
      if   (this.volume === 0) {
        this.$refs.audio.pause(); // 静音时停止播放
      } else {
        this.$refs.audio.play(); // 非静音时播放
      }
    },
  },
  
};

</script>


<!-- -------------------------------------------------
--------------------------------------------------
-------------------------------------------------
-------------------------------------------------------
------------------------------------------------------- -->
<!-- // 元素样式与美化 -->
<style scoped lang="scss">


.app {
     position: relative; // 确保父容器为相对定位
  min-height: 100vh; // 设置最小高度为视口高度
  display: flex;
  flex-direction: column; /* 垂直排列子元素 */
}

#navv {
  position: relative;
  list-style: none;
  background: #64beff91;
  box-shadow: 20px 60px 60px #00000033;
  padding: 15px;
}

#navv li {
  display: inline-block;
  position: relative;
}

#navv a {
  position: relative;
  padding: 15px 100px;
  font: 500 24px '优设标题黑';
  font-weight: bold;
  border: none;
  outline: none;
  color: rgb(43, 68, 137);
  text-decoration: none;
  z-index: 1;
}





.bg {
  position: absolute; /* 绝对定位 */
  top: 0; /* 距离顶部 */
  left: 0; /* 距离左边 */
  width: 100%; /* 宽度为100% */
  height: 100%; /* 高度为100% */
   
   background-image: url(@/assets/topbjtp.jpg);//设置背景图片路径 
    background-position: center; /* 使背景图片居中显示 */
    background-repeat: repeat; /* 不重复背景图片 */
  z-index: -3;
    
}
  
  


.header {
  flex: 1;
  position: relative;
}

header h1 {
   position: relative;
    /* 为标题添加样式 */
  font-size: 2.8rem;
  margin: 50px;

  font-weight: 700;
  color: #091c2e;
  text-transform: uppercase; //字母变大写
  letter-spacing: 0.05rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1); 
  border-bottom: 3.5px solid #0f4c82; 
  padding-bottom: 0.5rem;        
  //line-height: 1.2;     设置行高为1.2倍字体大小     
  position: relative;   

  display: block;
  box-sizing: border-box;
  animation: border-animate 3s linear infinite;
}

@keyframes border-animate {
  0%,100%{clip-path: inset(0 0 0 0);}
  25%{clip-path: inset(0 0 0 0);}
  50%{clip-path: inset(0 0 0 0);}
  75%{clip-path: inset(0 0 2% 0);}


}

.filter-box{

  margin-left: 17%;
  margin-top: 2rem;
}

// 轮播图整体样式
.teacher-carousel{
  margin-top: 20px; /* 上边距 */
  margin-right: 60px; /* 右边距 */
  margin-left: 60px; /* 左边距 */
}

.el-carousel__item {
  width:50% ; /* 设置轮播项的宽度为 20%，这样 5 个轮播项可以同时显示 */
}  

.el-carousel__item img {
 width: 100%; /* 根据需要调整照片大小 */
  height: 310px; /* 设置照片高度 */
  // border-radius: 50%; /* 使照片呈现圆形 */
  box-shadow: 0 10px 10px 0 rgba(0,0,0,0.2); /* 卡片阴影 */
  
}

.teacher-photo {
  width: 100%; /* 根据需要调整照片大小 */
  height: 200px; /* 设置照片高度 */
  border-radius: 50%; /* 使照片呈现圆形 */
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* 卡片阴影 */
  object-fit: cover; /* 图片缩放 */
  overflow: hidden; /* 防止图片溢出容器 */
}  
// 整个老师卡片的样式
.teacher-cards {
  margin-right: 60px;  /* 右边距 */
  margin-bottom: 50px; /* 下边距 */
  margin-left: 50px;   /* 左边距 */
  
}


// 卡片间的距离
.teacher-card {
 
  background-color: #c6e2f1; /* 卡片背景色 */
   width:  calc(95% - 10px); /* 卡片宽度，减去间距 */
   margin: 20px; /* 卡片间距 */
  height: 300px; /* 卡片高度 */
  transition: transform 0.3s ease-in-out;
   display: flex; /* 使用Flexbox */
  flex-direction: column; /* 垂直堆叠子元素 */
  align-items: center; /* 水平居中子元素 */
  justify-content: center; /* 垂直居中子元素（如果需要）*/
}
  
.teacher-card:hover {
  transform: translateY(-20px);
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
}  

.teacher-title {
  font-size: 14px;
  color: #444444;
  text-align: center;
}  

.teacher-info {
  font-weight: 550;
  text-align: center;
}  

.pagination {
  display: flex;
  justify-content: center;
  margin-bottom: 10%;
}

.filter-buttons {
  display: flex;
  justify-content: flex-start;     /* 左对齐排列按钮 */
  margin-top: 1rem;
  gap: 1.5rem;                /* 增加按钮之间的间距 */
}

.filter-buttons button {
  background-color: #ffffff;
  color: rgb(0, 0, 0);
  border: none;
  border-radius: 7px;
  padding: 0.5rem 1rem; 
  font-size: 1rem;
  //font-weight: 600;  /*字体粗细*/
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease; 
  box-shadow: 0 4px 1px rgba(0, 0, 0, 0.1); 
}


.filter-buttons button:hover {
/* 按钮悬浮效果 */
  background-color: #2980b9; 
  transform: translateY(-5px); 
}



.filter-buttons button:active {
  background-color: #1f6395;
  transform: translateY(0);
}

.filter-buttons button.active {
  // background-color: #2c3e50;
  background-color:#1f6395; 
}

.filter-buttons button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.4); 
}

.waveWrapper {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;

  overflow: hidden;
  z-index: -2;
}

.waveWrapperInner {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  
  // background-image: linear-gradient(to top, #86377b 20%, #27273c 80%, #1a1a2b 100%);
  // background-image: linear-gradient(to top,#b3e3df,#b3d3ef,#9cacd0, #91defe 50%, #99c0f9 , #b6bcec );
  background-image: linear-gradient(to top,rgba(179, 227, 223,1.1), rgba(179, 211, 229, 0.9), rgba(156, 172, 222, 0.7), rgba(145, 209, 254, 0.5), rgba(153, 192, 255, 0.3), rgba(182, 188, 206, 0.2) );
  //animation: wave 15s linear infinite;
}


.bgTop {
  z-index: -1;
  opacity: 0.5;
}
.bgMiddle {
  z-index: -2;
  opacity: 0.75;
}
.bgBottom {
  z-index: -3;
  opacity: 0.75;
}

.wave {
  position: absolute;
  bottom: 0;
  width: 200%;
  height: 100%;
  background-repeat: repeat no-repeat;
  background-position:0 bottom;
  transform-origin: center bottom;
   animation: move_wave 15s linear infinite;
}
@keyframes move_wave {
  0% {
    transform: translateX(0) translateZ(0) scaleY(1)
  }
  50% {
    transform: translateX(-25%) translateZ(0) scaleY(0.55)
  }
  100% {
    transform: translateX(-50%) translateZ(0) scaleY(1)
  }
}

.waveTop {
  background-size: 50% 100px;
  animation: move_wave 3s;
  animation-delay: 20s;
}

.waveMiddle {
  background-size: 50% 120px;
  animation: move_wave 10s linear infinite;
}

.waveBottom {
  background-size: 50% 140px;
  animation: move_wave 15s linear infinite;
}

.slider-block {
  max-width: 100%;
  display: flex;
  align-items: center;
}
.slider-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
  margin-right: 12px;
}

.no-teachers {
  text-align: center;
  font-size: 1.2rem;
  color: #888;
  margin-top: 20px;
  margin-bottom: 20px;
  display: block; margin-left: auto; margin-right: auto;
}

</style>
