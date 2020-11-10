<template lang="pug">
v-app(style="background-color: #EEE")
  v-main
    MemoryTable
</template>

<script>
import MemoryTable from './components/MemoryTable';

export default {
  name: 'App',
  components: {
    MemoryTable,
  },
  data: () => ({
    //
  }),
};
</script>
