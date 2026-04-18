<template>
  <router-view />
</template>

<style>
/* 桌面端优化 */
@media (min-width: 768px) {
  body {
    background-color: #f5f5f5;
  }
  #app {
    max-width: 500px;
    margin: 0 auto;
    background-color: #fff;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
    min-height: 100vh;
  }
}
</style>

