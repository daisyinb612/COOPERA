<template>
  <div>
    <GCharacter />
  </div>
</template>

<script>
import GCharacter from '../components/GCharacter.vue'; 
import { mapState } from 'vuex';


export default {
  name: 'PageOne',
  components: {
    GCharacter
  },
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
