<template lang="pug">
v-container
  v-row
    v-col.col-8
      v-card.col-12.pb-10#memory
        v-card-title メモリ
        v-row.justify-space-around(no-gutters)
          v-col.col-5
            v-card-title テキスト領域 + データ領域
            v-expansion-panels( multiple focusable accordion )
              v-expansion-panel(v-for="item in static" :key="item.address" :disabled="item.name == 'Unanalyzed'" @click="update()" :class="item.isChanged ? 'yellow lighten-5' : 'white'")
                v-expansion-panel-header(:id="item.address")
                  | {{ item.address}}
                  v-divider.mx-4( vertical style="color: black")
                  | {{ item.name }}
                v-expansion-panel-content.pt-4
                  pre.stack-data
                    p( v-text="`type : ${ item.type }`" )
                    p raw  : {{ item.raw }}
          v-col.col-5
            v-card-title スタック領域
            v-expansion-panels( multiple focusable accordion :value="activePanels" )
              v-expansion-panel(v-for="item in stack" :key="item.address" :disabled="item.name == 'padding'" @click="update()" :class="item.isChanged ? 'yellow lighten-5' : 'white'" )
                v-expansion-panel-header(:id="item.address" :ref="item.address")
                  | {{ item.address}}
                  v-divider.mx-4( vertical style="color: black")
                  | {{ item.name }}
                v-expansion-panel-content.pt-4
                 pre.stack-data
                  p( v-text="`scope : ${ item.scope }`" )
                  p( v-text="`type  : ${ item.type }`" )
                  template(v-if="isPointer(item)" )
                    p ref   : 
                      a(@click="" ) *{{ item.name }}
                      //- a(:href="`#${item.data.split('(')[0]}`") *{{ item.name }}
                  template(v-if="item.name === 'return infomation'")
                    div(:id="item.address + '-wrap'")
                      p data  : {
                      p(:id="item.address + '-fp'")  FP : {{ item.data.fp }}
                      p(:id="item.address + '-pc'")  PC : {{ item.data.pc }}
                      p }
                  p(v-else) data  : {{ item.data }}
                  p raw   : {{ item.raw }}
    v-col.col-4
      v-row(no-gutters)
        v-col.col-12
          v-card
            v-card-title プロセス
            v-card-text
              v-container
                v-row.text-center
                  v-col.col-3
                    v-tooltip( bottom )
                      template( v-slot:activator="{ on, attrs }" )
                        v-btn(icon small v-bind="attrs" v-on="on" @click="doProcess('CONTINUE')")
                          v-icon mdi-step-forward
                      span Continue
                  v-col.col-3
                    v-tooltip( bottom )
                      template( v-slot:activator="{ on, attrs }" )
                        v-btn( @click="doProcess('STEP_OVER')" icon small v-bind="attrs" v-on="on" )
                          v-icon mdi-debug-step-over 
                      span Step Over
                  v-col.col-3
                    v-tooltip( bottom )
                      template( v-slot:activator="{ on, attrs }" )
                        v-btn( @click="doProcess('STEP_INTO')" icon small v-bind="attrs" v-on="on" )
                          v-icon mdi-debug-step-into
                      span Step Into
                  v-col.col-3
                    v-tooltip( bottom )
                      template( v-slot:activator="{ on, attrs }" )
                        v-btn( @click="doProcess('STEP_OUT')" icon small v-bind="attrs" v-on="on" )
                          v-icon mdi-debug-step-out
                      span Step Out
                  v-col.col-12
                   v-overlay(absolute :value="overlay" )
                     v-btn.success( @click="flowOfProcess()" ) next
        v-col.col-12
          v-card.mt-10
            v-card-title デバッガ
            v-card-text
              v-container.align-center
                v-row
                  v-col.col-12
                    p.text--primary status: {{ status }}
                  v-col.col-6
                    v-select( v-model="breakpointLines" :items="[11,13,20,25]" label="breakpoint"  multiple dense )
                  v-col( style="text-align: center;" )
                    v-btn.primary( @click="setBreakpoints" ) set
                  v-col.col-12
                    v-switch( label="show breakpoints" v-model="breakpoints.show")
                    template( v-if="breakpoints.show" )
                      p {{ breakpoints.text }}
                v-row.justify-center
                  v-btn.mr-8.red( dark @click="launchLLDB" ) launch
                  v-btn.mr-8.primary( dark @click="stopLLDB" ) stop
        v-col.col-12
          v-card.mt-10#register
            v-card-title レジスタ
            v-card-text.ml-8.subtitle-1.text--primary
              pre(style="width: 50%")
                p#sp.pl-2(:class="previousData && register.sp !== previousData.register.sp ? 'red--text' : false") SP: {{ register.sp }}
                div(id="register-wrap")
                  p#fp.pl-2(:class="previousData && register.fp !== previousData.register.fp ? 'red--text' : false") FP: {{ register.fp }}
                  p#pc.pl-2(:class="previousData && register.pc !== previousData.register.pc ? 'red--text' : false") PC: {{ register.pc }}
</template>

<script>
import * as R from 'ramda';
import LeaderLine from 'leader-line-vue';

export default {
  name: 'App',
  data: () => ({
    breakpoints: {
      show: true,
      text: '',
    },
    breakpointLines: [13],
    status: 'stop',
    previousData: '',
    stack: [],
    activePanels: [],
    responseStore: {},
    register: {},
    static: {},
    lines: { register: null },
    previousLine: null,
    overlay: false,
    dataSizeDiff: 0
  }),
  methods: {
    initialize () {
      this.breakpoints = { show: true, text: '' };
      this.breakpointLines = [20];
      this.status = 'stop';
      this.previous = [];
      this.stack = [];
      this.register = {};
      this.static = {};
      this.lines = {};
      this.previousLine = null;
    },
    doProcess (type) {
      this.previousData = {
        stack: this.stack,
        register: this.register,
        static: this.static
      };
      this.$axios.get(`/api/process/${type}`).then(res => {
        this.dataSizeDiff = res.data.stack.length - this.stack.length;
        this.parseResponse(res.data);
        this.static = res.data.static;
        if (this.dataSizeDiff !== 0) {
          this.overlay = true;
          this.responseStore = res.data;
          this.flowOfProcess();
        } else {
          this.stack = res.data.stack;
          this.register = res.data.register[0];
        }
      }).catch(e => console.error(e));
    },
    parseResponse (res) {
      const addIsChangedProps = attr => obj => {
        const previous = R.find(R.propEq('address', obj.address))(this.previousData[attr]);
        obj.isChanged = !previous || !R.eqProps('raw', obj, previous); 
      };
      R.forEach(addIsChangedProps('stack'), res.stack);
      R.forEach(addIsChangedProps('static'), res.static);
      if (this.dataSizeDiff > 0) this.stack = res.stack.slice(this.dataSizeDiff);
    },
    flowOfProcess () {
      const diffType = Math.sign(this.dataSizeDiff);
      if (this.lines.register) {
        this.lines.register.remove();
        this.lines.register = null;
        this.register = this.responseStore.register[0];
        this.activePanels = [];
      }
      /* -- stack: push or pop --*/
      if (diffType === 1) { // positive
        const pushData = this.responseStore.stack[this.dataSizeDiff - 1];
        this.stack.unshift(pushData);
        this.dataSizeDiff -= 1;
      } else if (diffType === -1) { // negative
        this.stack.shift();
        this.dataSizeDiff += 1;
      }
      /* ------------------ */
      if (this.stack[0].name === "return infomation") {
        this.activePanels.push(this.stack.length-1); // open panel of new stack
        setTimeout(() => { // wait rendering
          const data = { element: document.getElementById(this.stack[0].address + '-wrap'), socket: 'right' };
          const register = { element: document.getElementById('register-wrap'), socket: 'left' };
          const startLine = diffType === 1 ? register : data;
          const endLine = diffType === 1 ? data : register;
          const options = { path: 'grid', startSocket: startLine.socket, endSocket: endLine.socket, hide: true, dash: { animation: true }};
          this.lines.register = LeaderLine.setLine(LeaderLine.obj.areaAnchor(startLine.element), LeaderLine.obj.areaAnchor(endLine.element), options);
          this.lines.register.show('draw'); // use animation
          this.register = this.responseStore.register[1];
        }, 100);
      }
      if (this.dataSizeDiff === 0) {
        this.overlay = false;
        this.stack = this.responseStore.stack;
        this.static = this.responseStore.static;
      }
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
          this.stack = res.data.stack;
          this.register = res.data.register[0];
          this.static = res.data.static;
        }
      });
    },
    stopLLDB () {
      this.$axios.get('/api/process/STOP').then(res => {
        if (res.status === 200) {
          this.initialize();
        }
      });
    },
    openInformation (item) {
      this.dialog.show = !this.dialog.show;
      if (this.dialog.show) {
        this.dialog.item = item;
      }
    },
    isPointer (item) {
      if (!item.type.includes('*')) return false;
      setTimeout(function() {
        this.addLeaderLine(item.address, item.data);
      }.bind(this), 500);
      return true;
    },
    addLeaderLine(startId, endId) {
      const startComponent = this.$refs[startId] ? this.$refs[startId][0] : null;
      const endElement = document.getElementById(this.preferredId(endId));
      if (!startComponent || !endElement ) return;
      const options = {
        path: 'grid',
        startSocket: endId.length !== 18 ? 'left' : 'right',
        endSocket: 'right',
        hide: true
      };
      this.lines[startId] = LeaderLine.setLine(startComponent.$el, endElement, options);
      // const aLine = LeaderLine.setLine(startComponent.$el, endElement, options);
      // this.lines[startId] = aLine;
    },
    preferredId (id) {
      return id.length !== 18 ? id.slice(0, 18) : id;
    },
    update() {
      setTimeout(() => {
        Object.keys(this.lines).forEach(key => {
          const aComponent = this.$refs[key][0];
          const aLine = this.lines[key];
          aLine.position();
          if (aComponent.isActive) aLine.show();
          else aLine.hide();
        });
      }, 300);
    }
  }
};
</script>

<style>
.stack-data {
  white-space: pre-wrap;
}
.leader-line, .leader-line-areaAnchor {
  z-index: 1;
}
</style>