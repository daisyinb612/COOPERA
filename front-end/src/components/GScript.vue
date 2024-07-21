<template>
    <div>
      <p>当前故事线：{{ storyline }}</p>
    </div>
  </template>
  
  <script>
  import { mapState } from 'vuex';
  
  export default {
    computed: {
      ...mapState('logline', {
        storyline: state => state.storyline
      })
    }
  };
  </script>
  
  <style scoped>
  /* 添加你的样式 */
  </style>
  