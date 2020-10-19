<template lang="pug">
  v-card.mt-10.mx-auto(max-width="500")
    v-card-title Memory Table
      v-card-text(v-text="memory" style="white-space:pre-wrap; word-wrap:break-word;")
    v-card-actions.justify-center 
      v-btn.primary( @click="fetchMemory" ) memory
</template>

<script>
export default {
  name: 'App',
  data: () => ({
    memory: "None"
  }),
  methods: {
    fetchMemory () {
      this.$axios.get('/api/memory').then(res => {
        this.memory = res.data;
      }).catch(e => console.error(e));
    }
  }
};
</script>