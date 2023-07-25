<template>
  <a-row :gutter="16">
    <a-col class="gutter-row" :sm="24" :xl="12">
      <h2>标题摘要生成 &nbsp;<a-badge :status="status_icon" :text="status_text"/>
      </h2>

      <a-form-model :label-col="labelCol" :wrapper-col="wrapperCol">

        <a-form-model-item label="输入文本">
          <a-input v-model="input_contents" type="textarea" :auto-size="{ minRows: 10, maxRows:15 }"/>
        </a-form-model-item>

        <a-form-model-item label="摘要字数">
          <a-col :span="12">
            <a-slider v-model="summary_max_words" :min="100" :max="200"/>
          </a-col>
          <a-col :span="4">
            <a-input-number v-model="summary_max_words" :min="100" :max="200" style="marginLeft: 16px"/>
          </a-col>
        </a-form-model-item>

        <a-form-model-item :wrapper-col="{ span: 14, offset: 4 }">
          <a-button type="primary" :loading="status_icon == 'processing'" @click="showModal">
            生成
          </a-button>

          <a-button style="margin-left: 10px;" @click="reset">
            重置
          </a-button>
        </a-form-model-item>
      </a-form-model>

      <a-modal
          title="选择节点和模型"
          :visible="modal.visible"
          :confirm-loading="modal.confirmLoading"
          @ok="handleModalOk"
          @cancel="handleModalCancel"
      >
        <a-select :default-value="nodeList[0]" style="width: 220px" @change="handleProvinceChange">
          <a-select-option v-for="province in nodeList" :key="province">
            {{ province }}
          </a-select-option>
        </a-select>
        <a-select v-model="secondCity" style="width: 220px">
          <a-select-option v-for="city in cities" :key="city">
            {{ city }}
          </a-select-option>
        </a-select>
      </a-modal>


      <div v-if="this.status_icon == 'success' && this.real_status == true">
        <word-cloud :detail_id="sid"></word-cloud>

        <a-alert
            message="免责声明"
            description="当前体验服务生成的所有内容都是由人工智能模型生成，我们对其生成内容的准确性、完整性和功能性不做任何保证，并且其生成的内容不代表我们的态度或观点。本页面服务仅供学术测试，输入及生成的内容，禁止传播。"
            type="info"
            show-icon
        />
      </div>

    </a-col>
    <a-col class="gutter-row" :sm="24" :xl="12">
      <div>


        <div v-if="status_icon=='default'">
          <h2>服务状态</h2>
          <div v-if="statistics.loading">
            <a-skeleton active/>
          </div>
          <div v-else>
            <a-row style="padding-bottom: 20px">
              <a-col :span="10">
                <a-card>
                  <a-statistic
                      title="今日总计"
                      :value="statistics.today_sum"
                      :precision="0"
                      suffix="条"
                      :value-style="{ color: '#3f8600' }"
                      style="margin-right: 50px"
                  >
                    <template #prefix>
                      <a-icon type="form"/>
                    </template>
                  </a-statistic>
                </a-card>
              </a-col>

              <a-col :span="10">
                <a-card>
                  <a-statistic
                      title="待审核"
                      :value="statistics.unverify"
                      :precision="0"
                      suffix="条"
                      :value-style="{ color: '#cf1322' }"
                      style="margin-right: 50px"
                  >
                    <template #prefix>
                      <a-icon type="clock-circle"/>
                    </template>
                  </a-statistic>
                </a-card>
              </a-col>
            </a-row>

            <a-row style="padding-bottom: 20px" :gutter="12">
              <a-col :span="7">
                <a-card title="CPU">
                  <a-progress type="dashboard" :percent="statistics.cpu_percent"/>
                </a-card>
              </a-col>

              <a-col :span="7">
                <a-card title="内存">
                  <a-progress type="dashboard" :percent="statistics.mem_percent"/>
                </a-card>
              </a-col>
              <a-col :span="7">
                <a-card title="GPU">
                  <a-progress type="dashboard" :percent="0"/>
                </a-card>
              </a-col>
            </a-row>
          </div>


        </div>
        <div v-if="this.status_icon == 'success' && this.real_status == false">
          <a-skeleton active/>
        </div>
        <div v-if="this.status_icon == 'success' && this.real_status == true">
          <h2>查看结果</h2>
          <detail-page :detail_id="sid"></detail-page>
          <a-divider><span style="color: gray">感觉如何？</span></a-divider>
          <span @click="onRate(rate_value);">
          <a-rate v-model="rate_value" :tooltips="rate_desc"/>
          <span class="ant-rate-text">{{ rate_desc[rate_value - 1] }}</span>
        </span>
        </div>


      </div>


    </a-col>

  </a-row>

</template>

<script>

import axios from "axios";
import WordCloud from "@/components/WordCloud";
import DetailPage from "@/components/DetailPage";

const nodeList = ['超算云GPU区-TK节点', '测试备用GPU节点'];
const ModalList = {
  '超算云GPU区-TK节点': ['GPT2-2022.6'],
  '测试备用GPU节点': ['指针生成'],
};

export default {
  components: {DetailPage, WordCloud},
  beforeCreate: function () {
    this.HOST = process.env.VUE_APP_SERVER_URL;

  },
  mounted() {
    this.input_contents = this.exampleText;
    this.getStatus();
    this.timer = setInterval(this.getStatus, 5000);
  },

  data() {
    return {
      status_text: '准备开始',
      status_icon: 'default',

      real_status: false,

      sid: -1,

      summary_max_words: 0,
      exampleText: "岁月不居，时节如流。五年，弹指一挥间，“十三五”即将落子收官。这是“中国号”列车以风驰电掣的速度和时间赛跑的五年，是用速度跑出风采、用实干创造辉煌、用奋斗书写华章的五年。\\n在这场为期五年的“大考”中，中国在众多领域刷新成绩，跑出了中国新速度，交出了令世人惊叹的中国答卷。数据显示，2019年，我国GDP达99.1万亿元，对世界经济增长贡献达30%左右；2019年末，我国高速铁路营业总里程超过3.5万公里，占全球高铁里程2/3以上，高速公路里程超过14万公里，稳居世界第一；我国制造业增加值多年位居世界首位，工业持续壮大……五年筚路蓝缕，五年奋斗拼搏，中国速度惊艳世界，托举起亿万人民对幸福美好新生活的向往，驱动“中国号”列车加大马力，向着中华民族伟大复兴的目标全速前进。\\n中国速度彰显制度优势。中国速度如此之快，展示了国家实力，彰显了民族自信，也再一次充分证明了中国特色社会主义制度集中力量办大事的显著优势。今年新冠肺炎疫情期间，用10多天时间先后建成火神山医院和雷神山医院，在最短时间内实现了医疗资源和物资供应从紧缺向动态平衡的跨越式提升，第一时间研发出核酸检测试剂盒……中国速度再次令人惊叹，取得的巨大成就堪称奇迹，不仅体现了同舟共济、守望相助的家国情怀，更是中国制度优势的生动写照。\\n中国速度折射奋进姿态。时间不等人，历史不等人，只有锲而不舍不断奔跑，才能早日抵达梦想的彼岸。“十三五”时期的中国，“天眼”望天、“蛟龙”探海、大飞机首飞、高铁驰骋、超级计算机竞逐榜首、核电技术与装备“走出去”……一批标志性、引领性重大原创成果竞相涌现，一个又一个创造世界奇迹的中国速度，折射中国勇往直前的奋进姿态。正是无数普普通通的劳动者，以百倍努力、千倍艰辛、万倍执着，在各行各业创造出令世界惊叹的中国速度。中国的发展壮大是不可阻挡的历史潮流，正是亿万人民的奋勇拼搏，汇聚起推动历史车轮前进的中国力量，推动“中国号”列车不断加速前进。\\n五年风雨兼程，五年砥砺前行。五年来，中国发展含金量更高、动力更充沛、协调性更好、持续性更强。当下，脱贫攻坚冲锋号已经吹响，全面小康千年愿景即将梦圆。我们相信，在中国共产党的团结带领下，在全国人民的共同努力下，中国一定会创造更多令世界惊叹的新速度和新奇迹，在新的历史起点上迈向更加光明的未来。",
      input_contents: '',
      labelCol: {span: 4},
      wrapperCol: {span: 14},
      form: {},

      rate_value: -1,
      rate_desc: ['很糟糕', '比较差', '还不错', '优秀', '好极了'],

      statistics: {
        today_sum: 0,
        unverify: 0,
        cpu_percent: 0,
        mem_percent: 0,
        loading: true,
      },

      modal: {
        visible: false,
        confirmLoading: false
      },

      nodeList,
      ModalList,
      cities: ModalList[nodeList[0]],
      secondCity: ModalList[nodeList[0]][0],
    };
  },
  methods: {
    onSubmit() {

      if (!this.input_contents || this.input_contents.length <= 10) {
        this.$message.error('请输入不少于10字的原文！');
        return;
      }


      let formData = new FormData();
      formData.append('content', this.input_contents);
      formData.append('max_len', this.summary_max_words);

      axios.post(this.HOST + "/get_summary", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          "Authorization": window.localStorage.getItem('token'),
        }
      }).then(
          res => {
            let code = res.data['code'];
            let msg = res.data['msg'];

            if (code == 0) {
              //处理数据逻辑
              let ret = res.data['body'];
              this.sid = ret['sid'];

              this.real_status = true;

            } else {
              this.$message.error('错误信息：' + msg);
              this.status_icon = 'error';
              this.status_text = '处理失败';

            }

          }
      ).catch(error => {
            this.$message.error('网络错误：' + error);
            this.status_icon = 'error';
            this.status_text = '处理失败';
          }
      )

    },
    onRate(rate_value) {
      axios.get(this.HOST + "/user_rate", {
        params: {
          sid: this.sid,
          value: rate_value,
        }
      }).then(
          res => {
            console.log(res.data);
            this.$message.success("感谢您的评价，我们会继续努力！");

          }
      ).catch(
          error => {
            this.$message.error('错误信息：' + error);
          }
      )

    },
    reset() {
      this.status_icon = 'default';
      this.status_text = '准备开始';
      this.input_contents = '';
      this.real_status = false;

    },
    getStatus() {
      axios.get(this.HOST + "/status", {}).then(
          // 使用箭头函数this才会指代当前的Vue对象，如果使用的是function()，this指代的是window对象
          res => {
            console.log(res.data);
            this.statistics.today_sum = res.data['body']['today_sum'];
            this.statistics.unverify = res.data['body']['today_unverify'];
            this.statistics.cpu_percent = parseFloat(res.data['body']['cpu']);
            this.statistics.mem_percent = parseFloat(res.data['body']['mem']);

            this.statistics.loading = false;

          }
      )

    },
    showModal() {
      this.onSubmit();
      this.modal.visible = true;
    },
    handleModalOk() {
      this.modal.confirmLoading = true;
      this.status_icon = 'processing';
      this.status_text = '正在生成';
      this.statistics.loading = true;

      setTimeout(() => {
        this.modal.visible = false;
        this.modal.confirmLoading = false;
        this.status_icon = 'success';
        this.status_text = '处理完毕';

      }, 1000);


    },
    handleModalCancel() {
      this.modal.visible = false;
    },
    handleProvinceChange(value) {
      this.cities = ModalList[value];
      this.secondCity = ModalList[value][0];
    },
  }
}
</script>

<style scoped>

</style>