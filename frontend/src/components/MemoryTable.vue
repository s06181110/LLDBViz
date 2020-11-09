<template lang="pug">
v-container
  v-card.mx-auto.mt-10( max-width="600" )
    v-card-title Process
    v-card-text
      v-container
        v-row.text-center
          //
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
  v-card.mx-auto.my-10.pb-6( max-width="600" )
    v-card-title Stack Memory
    v-card( elevation="16" class="mx-auto" max-width="500"  )
      v-virtual-scroll( :items="stack" :bench="stack.length" item-height="64" max-height="500")
          template( v-slot:default="{ item }" )
            v-list-item( :key="item.address" :id="item.address" link )
              v-list-item-content( style="width: 150px" )
                v-list-item-title {{ item.address }}
              v-divider.mx-4(vertical)
              v-list-item-content
                v-list-item-title {{ item.name }}
              v-list-item-action
                v-btn( icon depressed small @click="openInformation(item)" )
                  v-icon mdi-information-outline
            v-divider( v-if="item.address != stack[stack.length - 1].address")
    v-dialog( v-model="dialog.show " width="500" v-if="dialog.show" )
      v-card(style="white-space:pre-wrap;")
        v-card-title information
        v-card-text
          p( v-text="`address: ${ dialog.item.address }`" )
          p( v-text="`type: ${ dialog.item.type }`" )
          p name: {{ dialog.item.name }}
            template(v-if="isPointer(dialog.item.type)" )
              | →
              a(:href="`#${dialog.item.data.split('(')[0]}`" @click="dialog.show = false")  *{{ dialog.item.name }}
          p data   : {{ dialog.item.data }}
          p raw    : {{ dialog.item.raw }}
      //
        v-card-text(v-text="`address: ${ dialog.item.address }`" )
        v-card-text(v-text="`type: ${ dialog.item.type }`" )
        template(v-if="isPointer(dialog.item.type)" )
          v-card-text(v-text="`name: ${ dialog.item.name } → `" )
            a(:href="`#${dialog.item.address}`") {{ dialog.item.name }}
        v-card-text data   : {{ dialog.item.data }}
        v-card-text raw    : {{ dialog.item.raw }}
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
    breakpointLines: [13],
    status: 'stop',
    stack: [],
    dialog: {
      show: false,
      item: {},
    }
  }),
  methods: {
    doProcess (type) {
      this.$axios.get(`/api/process/${type}`).then(res => {
        console.log(res.data);
        this.stack = res.data;
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
          console.log(res.data);
          this.stack = res.data;
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
    },
    valueToAddress(value) {
      const addr = value.split(' ').slice(-1);
      return '0x' + parseInt(addr, 16).toString(16); // 0x00ff -> 0xff
    },
  }
};
</script>