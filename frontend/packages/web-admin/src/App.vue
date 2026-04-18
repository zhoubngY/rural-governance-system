<template>
  <router-view />
</template>

<style>
/* 全局基础样式 */
body {
  background-color: #f5f5f5;
  margin: 0;
  padding: 0;
}

/* 移动端默认样式 */
#app {
  width: 100%;
  background-color: #fff;
  min-height: 100vh;
}

/* 电脑端优化：宽度限制更宽，居中显示，添加阴影 */
@media (min-width: 768px) {
  body {
    background-color: #e9ecef;
  }
  #app {
    max-width: 1200px;   /* 电脑端最大宽度增大 */
    margin: 0 auto;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    border-radius: 8px;   /* 可选圆角 */
    overflow: hidden;     /* 保证圆角生效 */
  }
}

/* 超大屏幕（>1400px）可进一步增加宽度 */
@media (min-width: 1400px) {
  #app {
    max-width: 1400px;
  }
}
</style>