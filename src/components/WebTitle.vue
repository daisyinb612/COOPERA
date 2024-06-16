<template>
    <div :class="$style.title">
      <div :class="$style.ellipseParent">
        <div :class="$style.frameChild"></div>
        <div :class="$style.coOpera">CO-OPERA</div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "WebTitle"
  }
  </script>
  
  <style module>
  .frameChild {
    width: 50px;
    position: relative;
    box-shadow: 0px 4px 4px 4px rgba(0, 0, 0, 0.1) inset, 0px 4px 4px 4px rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    background: linear-gradient(162.86deg, #a1b0ff, #f472ff);
    border: 4px solid rgba(255, 255, 255, 1);
    box-sizing: border-box;
    height: 50px;
  }
  
  .coOpera {
    position: relative;
    font-weight: 800;
  }
  
  .ellipseParent {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: 20px;
  }
  
  .title {
    width: 100%;
    position: relative;
    background: linear-gradient(162.86deg, #a1b0ff, #f472ff);
    height: 80px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 17px 20px;
    box-sizing: border-box;
    text-align: left;
    font-size: 36px;
    color: #fff;
    font-family: var(--font-jetbrains-mono);
  }
  </style>  