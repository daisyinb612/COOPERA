<template>
  <el-row :class="$style.menu">
    <div :class="$style.menuInner">
      <el-button :class="[ $style.inputLoglineWrapper, isActive('/home/inputlogline') ? $style.active : '' ]" @click="goToPage('/home/inputlogline')" plain>
        <div :class="$style.inputLogline">input logline</div>
      </el-button>
    </div>
    <div :class="$style.menuChild">
      <div :class="$style.frameParent">
        <el-button :class="[ $style.inputLoglineWrapper, isActive('/home/pageone') ? $style.active : '' ]" @click="goToPage('/home/pageone')" plain>
          <div :class="$style.frameGroup">
            <el-icon :class="$style.icon">
              <User />
            </el-icon>
            <div :class="$style.charater">Character</div>
          </div>
        </el-button>
        <el-button :class="[ $style.inputLoglineWrapper, isActive('/home/pagetwo') ? $style.active : '' ]" @click="goToPage('/home/pagetwo')" plain>
          <div :class="$style.frameGroup">
            <el-icon :class="$style.icon">
              <edit />
            </el-icon>
            <div :class="$style.charater">Plot</div>
          </div>
        </el-button>
        <el-button :class="[ $style.inputLoglineWrapper, isActive('/home/pagethree') ? $style.active : '' ]" @click="goToPage('/home/pagethree')" plain>
          <div :class="$style.frameGroup">
            <el-icon :class="$style.icon">
              <Location />
            </el-icon>
            <div :class="$style.charater">Location</div>
          </div>
        </el-button>
        <el-button :class="[ $style.inputLoglineWrapper, isActive('/home/pagefour') ? $style.active : '' ]" @click="goToPage('/home/pagefour')" plain>
          <div :class="$style.frameGroup">
            <el-icon :class="$style.icon">
              <Reading />
            </el-icon>
            <div :class="$style.charater">Dialogue</div>
          </div>
        </el-button>
      </div>
    </div>
    <div :class="$style.menuInner">
      <el-button :class="[ $style.inputLoglineWrapper, isActive('/home/renderscript') ? $style.active : '' ]" @click="goToPage('/home/renderscript')" plain>
        <div :class="$style.inputLogline">render script</div>
      </el-button>
    </div>
  </el-row>
</template>

<script>
import { defineComponent } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { Edit } from '@element-plus/icons-vue';

export default defineComponent({
  name: 'MenuGuide',
  components: {
    Edit
  },
  setup() {
    const router = useRouter();
    const route = useRoute();

    const goToPage = (path) => {
      router.push(path);
    };

    const isActive = (path) => {
      return route.path === path;
    };

    return {
      goToPage,
      isActive
    };
  }
});
</script>

<style module>
.menu {
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 20px 0;
  box-sizing: border-box;
  text-align: center;
  font-size: 20px;
  color: #000;
  font-family: 'JetBrains Mono';
}

.inputLogline {
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.inputLoglineWrapper {
  color: #000;
  background-color: #d5dcff;
  border: 2px solid #5973FF;
  width: 250px;
  border-radius: 20px;
  height: 60px;
  overflow: hidden;
  flex-shrink: 0;
  margin-top: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  text-align: left;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.inputLoglineWrapper:hover {
  color: #8AABFF;
  background-color: #d5dcff;
  border: 2px solid #5973FF;
}

.inputLoglineWrapper:active {
  color: #ffffff;
  background-color: #8AABFF;
  border: 2px solid #5973FF;
}

.active {
  color: #ffffff;
  background-color: #8AABFF;
  border: 2px solid #5973FF;
}

.menuInner {
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 25px;
}

.frameChild {
  width: 30px;
  position: relative;
  height: 30px;
  overflow: hidden;
  flex-shrink: 0;
}

.charater {
  display: flex;
  align-items: center;
  font-weight: 600;
  flex-shrink: 0;
}

.frameGroup {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 5px;
}

.frameParent {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 10px 0;
  gap: 20px;
}

.menuChild {
  overflow: hidden;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 15px 25px;
  text-align: left;
}

.content {
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #F5F5F5;
}

.inputLoglineWrapper + .inputLoglineWrapper {
  margin-left: 0 !important;
}
</style>