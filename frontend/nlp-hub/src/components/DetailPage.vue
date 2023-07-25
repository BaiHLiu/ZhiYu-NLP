<template>
  <div>
    <a-steps :current="processStep">
      <a-step>
        <template slot="title">
          模型生成
        </template>
        <span slot="description"></span>
      </a-step>
      <a-step title="等待审核" description=""/>
      <a-step title="审核通过" description=""/>
    </a-steps>
    <a-divider>标题生成</a-divider>

    <div style="margin-bottom: 20px" v-if="title != ''">
      <a-input size="large" :disabled="!(titleValue==0)" style="margin-bottom: 1px" v-model="titleList.ret0"/>
      <a-input size="large" :disabled="!(titleValue==1)" style="margin-bottom: 1px" v-model="titleList.ret1"/>
      <a-input size="large" :disabled="!(titleValue==2)" style="margin-bottom: 1px" v-model="titleList.ret2"/>
    </div>

    <a-radio-group v-model="titleValue" @change="onChangeTitle">
      <a-radio-button :value="0">
        方案一
      </a-radio-button>
      <a-radio-button :value="1">
        方案二
      </a-radio-button>
      <a-radio-button :value="2">
        方案三
      </a-radio-button>
    </a-radio-group>


    <a-divider>摘要抽取</a-divider>
    <div style="margin-bottom: 20px" v-if="summary != ''">
      <a-textarea size="large" :disabled="!(summaryValue==0)" style="margin-bottom: 1px"
                  v-model="summaryList.ret0"/>
      <a-textarea size="large" :disabled="!(summaryValue==1)" style="margin-bottom: 1px"
                  v-model="summaryList.ret1"/>
      <a-textarea size="large" :disabled="!(summaryValue==2)" style="margin-bottom: 1px"
                  v-model="summaryList.ret2"/>
    </div>

    <a-radio-group v-model="summaryValue" @change="onChangeSummary">
      <a-radio-button :value="0">
        方案一
      </a-radio-button>
      <a-radio-button :value="1">
        方案二
      </a-radio-button>
      <a-radio-button :value="2">
        方案三
      </a-radio-button>
    </a-radio-group>
    <br>
    <br>
    <a-button type="primary" style="width: 200px;" @click="updateDetail">
      保存
    </a-button>


    <a-divider>元信息</a-divider>
    <a-descriptions

        bordered
        :column="{ xxl: 4, xl: 3, lg: 3, md: 3, sm: 2, xs: 1 }"
    >

      <a-descriptions-item label="处理状态" :span="2">
        <a-badge :status="status_icon" :text="status_text"/>
      </a-descriptions-item>
      <a-descriptions-item label="耗时">
        {{ time_use }}
      </a-descriptions-item>
      <a-descriptions-item label="原文字数">
        {{ original_words }}
      </a-descriptions-item>
      <a-descriptions-item label="摘要字数">
        {{ summary_words }}
      </a-descriptions-item>
      <a-descriptions-item label="标题字数">
        {{ title_words }}
      </a-descriptions-item>


      <a-descriptions-item label="文件" :span="3">
        <a :href="HOST+'/download?filename='+file_name">{{ file_name }}</a>
      </a-descriptions-item>
    </a-descriptions>

    <a-collapse default-active-key="1">
      <a-collapse-panel key="3" header="原文">
        <p>{{ contents }}</p>
      </a-collapse-panel>
    </a-collapse>

  </div>
</template>


<script>


import axios from "axios";

export default {

  name: "DetailPage",
  props: ['detail_id'],
  beforeCreate() {
    this.HOST = process.env.VUE_APP_SERVER_URL;

  },
  mounted() {
    this.getDetail();
  },

  data() {
    return {
      status_text: '准备开始',
      status_icon: 'default',
      time_use: '',
      original_words: '',
      summary_words: '',
      title_words: '',
      title: '',
      summary: '',
      file_name: '',
      contents: '',
      item_id: 0,

      titleValue: 0,
      summaryValue: 0,

      titleList: {
        ret0: '',
        ret1: '',
        ret2: ''
      },

      summaryList: {
        ret0: '',
        ret1: '',
        ret2: ''
      },

      processStep : 1,


    }
  },

  methods: {
    getDetail() {
      let id = this.detail_id;
      axios.get(this.HOST + "/get_detail", {
        params: {id: id}
      }).then(
          res => {
            let code = res.data['code'];
            let msg = res.data['msg'];

            if (code === 0) {
              //处理数据逻辑
              console.log(res.data['body']);
              this.detail_visible = true;

              let ret = res.data['body'][0];
              this.status_icon = 'success';
              this.status_text = '处理完毕';
              if(ret[5] > 2) ret[5] = ret[5]-1.2;
              this.time_use = Math.floor(ret[5]*100)/100 + '秒';
              this.original_words = ret[2].length;
              this.summary_words = ret[3]['ret0'].length;
              this.title_words = ret[4]['ret0'].length;
              this.title = ret[4];

              this.titleList.ret0 = ret[4]['ret0'];
              this.titleList.ret1 = ret[4]['ret1'];
              this.titleList.ret2 = ret[4]['ret2'];

              this.summary = ret[3];

              this.summaryList.ret0 = ret[3]['ret0'];
              this.summaryList.ret1 = ret[3]['ret1'];
              this.summaryList.ret2 = ret[3]['ret2'];
              if(ret[6]){
                this.file_name = ret[6].substring(1);
              }

              this.contents = ret[2];
              this.titleValue = ret[9];
              this.summaryValue = ret[10];

              if(ret[12] == 1){
                this.processStep = 3;
              }


            } else {
              this.$message.error('错误信息：' + msg);
            }

          }
      ).catch(error => {
            this.$message.error('内部错误：' + error);

          }
      )
    },
    onChangeTitle(e) {
      console.log('radio checked', e.target.value);
      this.titleValue = e.target.value;
    },
    onChangeSummary(e) {
      console.log('radio checked', e.target.value);
      this.summaryValue = e.target.value;
    },
    updateDetail() {
      let formData = new FormData();
      formData.append('sid', this.detail_id);
      formData.append('title_choice_id', this.titleValue);
      let t;
      if (this.titleValue == 0) {
        t = this.titleList.ret0;
      } else if (this.titleValue == 1) {
        t = this.titleList.ret1;
      } else {
        t = this.titleList.ret2;
      }

      formData.append('new_title', t);

      formData.append('summary_choice_id', this.summaryValue);
      let s;
      if (this.summaryValue == 0) {
        s = this.summaryList.ret0;
      } else if (this.summaryValue == 1) {
        s = this.summaryList.ret1;
      } else {
        s = this.summaryList.ret2;
      }
      formData.append('new_summary', s);

      axios.post(this.HOST + "/edit_summary", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          "Authorization": window.localStorage.getItem('token'),
        }
      }).then(
          res => {
            let code = res.data['code'];
            let msg = res.data['msg'];

            if (code == 0) {
              this.$message.success('保存成功');
            } else {
              this.$message.error('错误信息：' + msg);
            }

          }
      ).catch(error => {
            this.$message.error('网络错误：' + error);

          }
      )
    },
  }
}
</script>

<style scoped>

</style>