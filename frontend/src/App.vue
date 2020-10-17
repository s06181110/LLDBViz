<template lang="pug">
  v-app 
    HelloWorld
    v-card.red.lighten-4
      v-card-title Hoge
</template>

<script>
import HelloWorld from './components/HelloWorld';

export default {
  name: 'App',
  components: {
    HelloWorld,
  },
  data: () => ({
    //
  }),
};
</script>
