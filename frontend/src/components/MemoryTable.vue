<template lang="pug">
v-container
  v-row
    v-col.col-4
      v-row(no-gutters)
        v-col.col-12
          v-card
            v-card-title Script
            v-card-text comming soon
    v-col.col-4
      v-row(no-gutters)
        v-col.col-12
          v-card.pb-12
            v-card-title Stack Memory
            v-expansion-panels( multiple focusable accordion )
              v-expansion-panel(v-for="item in stack" :key="item.address")
                v-expansion-panel-header  
                  | {{ item.address}}
                  v-divider.mx-4( vertical style="color: black")
                  | {{ item.name }}
                v-expansion-panel-content.pt-4
                  p( v-text="`address: ${ item.address }`" )
                  p( v-text="`type: ${ item.type }`" )
                  p name: {{ item.name }}
                    template(v-if="isPointer(item.type)" )
                      | →
                      a(:href="`#${item.data.split('(')[0]}`") *{{ item.name }}
                  p data   : {{ item.data }}
                  p raw    : {{ item.raw }}
    v-col.col-4
      v-row(no-gutters)
        v-col.col-12
          v-card
            v-card-title Process
            v-card-text
              v-container
                v-row.text-center
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
        v-col.col-12
          v-card.mt-10
            v-card-title Debugger
            v-card-text
              v-container.align-center
                v-row
                  v-col.col-12
                    p.text--primary status: {{ status }}
                  v-col.col-6
                    v-select( v-model="breakpointLines" :items="[11,13,25]" label="breakpoint"  multiple dense )
                  v-col( style="text-align: center;" )
                    v-btn.primary( @click="setBreakpoints" ) set
                  v-col.col-12
                    v-switch( label="show breakpoints" v-model="breakpoints.show")
                    template( v-if="breakpoints.show" )
                      p {{ breakpoints.text }}
                v-row.justify-center
                  v-btn.mr-8.red( dark @click="launchLLDB" ) launch
                  v-btn.mr-8.primary( dark @click="stopLLDB" ) stop
        v-col.col-12(v-if="status === 'launch'" )
          v-card.mt-10
            v-card-title Register
            v-card-text
              p SP: {{ register.sp }}
              p FP: {{ register.fp }}
              p PC: {{ register.pc }}
</template>

<script>
// import * as R from 'ramda';

export default {
  name: 'App',
  data: () => ({
    breakpoints: {
      show: true,
      text: '',
    },
    breakpointLines: [25],
    status: 'stop',
    previous: [],
    stack: [],
    register: {},
    dialog: {
      show: false,
      item: {},
    }
  }),
  methods: {
    doProcess (type) {
      this.previous = this.stack;
      this.$axios.get(`/api/process/${type}`).then(res => {
        this.stack = res.data.memory;
        this.register = res.data.register;
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
          this.stack = res.data.memory;
          this.register = res.data.register;
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
    openInformation (item) {
      this.dialog.show = !this.dialog.show;
      if (this.dialog.show) {
        this.dialog.item = item;
      }
    },
    isPointer (type) {
      return type.includes('*');
    }
  }
};
</script>