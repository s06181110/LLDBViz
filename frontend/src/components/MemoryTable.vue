<template lang="pug">
v-container
  v-card.mx-auto.mt-10( max-width="600" )
    v-card-title Memory Table
    v-card-text
      v-container
        v-row
          v-col.col-12
            p(v-text="memory" style="white-space:pre-wrap; word-wrap:break-word;")
          v-col.col-3
            v-btn( @click="fetchMemory('CONTINUE')" icon small )
              v-icon mdi-step-forward
          v-col.col-3
            v-btn( @click="fetchMemory('STEP_OVER')" icon small )
              v-icon mdi-debug-step-over 
          v-col.col-3
            v-btn( @click="fetchMemory('STEP_INTO')" icon small )
              v-icon mdi-debug-step-into
          v-col.col-3
            v-btn( @click="fetchMemory('STEP_OUT')" icon small )
              v-icon mdi-debug-step-out
  v-card.mx-auto.mt-10( max-width="600" )
    v-card-title Variables
    v-card-text
      v-container
        v-row
          v-col.col-12
            p(v-text="variables" style="white-space:pre-wrap; word-wrap:break-word;")
  v-card.mx-auto.mt-10( max-width="600" )
    v-card-title Debugger
    v-card-text
      v-container.align-center
        v-row
          v-col.col-12
            p.text--primary status: {{ status }}
          v-col.col-6
            v-select( v-model="breakpointLines" :items="[11,13]" label="breakpoint"  multiple dense )
          v-col( style="text-align: center;" )
            v-btn.primary( @click="setBreakpoints" ) set
          v-col.col-12
            v-switch( label="show breakpoints" v-model="breakpoints.show")
            template( v-if="breakpoints.show" )
              p {{ breakpoints.text }}
        v-row.justify-center
          v-btn.mr-8.red( dark @click="launchLLDB" ) launch
          v-btn.blue-grey( dark @click="stopLLDB" ) stop
</template>

<script>
export default {
  name: 'App',
  data: () => ({
    memory: 'None',
    variables: 'None',
    breakpoints: {
      show: false,
      text: '',
    },
    breakpointLines: [11],
    status: 'stop',
  }),
  methods: {
    fetchMemory (type) {
      this.$axios.get(`/api/process/${type}`).then(res => {
        this.memory = res.data;
      }).catch(e => console.error(e));
      this.fetchVariables();
    },
    fetchVariables () {
      this.$axios.get(`/api/variables`).then(res => {
        this.variables = res.data;
      }).catch(e => console.error(e));
    },
    setBreakpoints () {
      this.$axios.post('/api/breakpoints', this.breakpointLines)
        .then(res => {
          this.breakpoints.text = res.data;
        });
    },
    launchLLDB () {
      this.$axios.get('/api/launch').then(res => {
        if (res.status === 200) {
          this.status = 'launch';
          this.fetchMemory();
        }
      });
      console.log('launch');
    },
    stopLLDB () {
      this.$axios.get('/api/process/STOP').then(res => {
        if (res.status === 200) {
          this.status = 'stop';
          this.fetchMemory();
        }
      });
    }
  }
};
</script>