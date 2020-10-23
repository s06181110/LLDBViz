<template lang="pug">
v-container
  v-card.mx-auto.mt-10( max-width="600" )
    v-card-title Memory Table
    v-card-text
      v-container
        v-row
          v-col.col-12
            template(v-if="table.length > 0" )
              template(v-for="value in table")
                p.my-15.py-15(:id="value.address") 
                  a(:href="'#' + valueToAddress(value.data)") {{ value.data }}
          v-col.col-3
            v-btn( @click="doProcess('CONTINUE')" icon small )
              v-icon mdi-step-forward
          v-col.col-3
            v-btn( @click="doProcess('STEP_OVER')" icon small )
              v-icon mdi-debug-step-over 
          v-col.col-3
            v-btn( @click="doProcess('STEP_INTO')" icon small )
              v-icon mdi-debug-step-into
          v-col.col-3
            v-btn( @click="doProcess('STEP_OUT')" icon small )
              v-icon mdi-debug-step-out
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
    breakpoints: {
      show: true,
      text: '',
    },
    breakpointLines: [13],
    status: 'stop',
    table: {},
  }),
  methods: {
    doProcess (type) {
      this.$axios.get(`/api/process/${type}`).then(res => {
        this.table = res.data;
      }).catch(e => console.error(e));
    },
    setBreakpoints () {
      this.$axios.post('/api/breakpoints', this.breakpointLines)
        .then(res => {
          this.breakpoints.show = true;
          this.breakpoints.text = res.data;
        });
    },
    launchLLDB () {
      this.$axios.get('/api/launch').then(res => {
        if (res.status === 200) {
          this.status = 'launch';
          this.table = res.data;
        }
      });
    },
    stopLLDB () {
      this.$axios.get('/api/process/STOP').then(res => {
        if (res.status === 200) {
          this.status = 'stop';
        }
      });
    },
    valueToAddress(value) {
      const addr = value.split(' ').slice(-1);
      return '0x' + parseInt(addr, 16).toString(16); // 0x00ff -> 0xff
    },
  }
};
</script>