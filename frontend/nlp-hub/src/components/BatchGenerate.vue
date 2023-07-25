<template>
  <div>
    <a-row :gutter="[24,16]">
      <a-col class="gutter-row" :sm="24" :xl="8">
        <h2>上传文件</h2>
        <div>
          <a-alert message="支持txt、docx格式的文档及zip压缩包。" type="info" show-icon/>
          <br>


          <a-upload
              :action="this.HOST + '/upload'"
              :multiple="true"
              :file-list="fileList"
              @change="handleChange"
              accept='.txt,.docx,.zip'
          >
            <a-button>
              <a-icon type="upload"/>
              上传
            </a-button>
          </a-upload>
          <br>
          <br>

          <a-button type="primary" block style="height: 40px" @click="make_summary();">
            开始处理
          </a-button>
        </div>

        <div style="text-align: center; margin-top: 30px; border: beige dotted">
          <h3>最新TOP10词云</h3>
          <word-cloud :detail_id="0"></word-cloud>
        </div>

      </a-col>
      <a-col class="gutter-row" :sm="24" :xl="16">
        <h2>查看进度</h2>
        <div>
          <HistoryList hide_time_use=true></HistoryList>
        </div>

      </a-col>
    </a-row>
  </div>
</template>

<script>
import HistoryList from '@/components/HistoryList';
import WordCloud  from "@/components/WordCloud";


import axios from "axios";

export default {
  name: "batch_generate",
  components: {HistoryList, WordCloud},


  beforeCreate: function () {
    this.HOST = process.env.VUE_APP_SERVER_URL;

  },



  data() {
    return {
      fileList: [
        {
          uid: '-1',
          name: '未选择文件',
          status: 'done',
        },
      ],
    };
  },
  methods: {

    handleChange(info) {
      let fileList = [...info.fileList];

      // 限制文件上传数量
      fileList = fileList.slice(-1);

      // 读取返回
      fileList = fileList.map(file => {
        if (file.response) {
          file.url = file.response.url;
          this.fileName = file.response;
        }
        return file;
      });

      this.fileList = fileList;
    },

    make_summary() {
      if (!this.fileName) {
        return this.$message.error('文件未上传!');
      }
      axios.get(this.HOST + "/get_file_summary", {
        headers:{
          "Authorization": window.localStorage.getItem('token'),
        },
        params: {
          filename: this.fileName
        }
      }).then(
          res => {
            let code = res.data['code'];
            let msg = res.data['msg'];

            if (code == 0) {
              //处理数据逻辑
              this.$message.success(msg);

            } else {
              this.$message.error('错误信息：' + msg);

            }

          }
      ).catch(error => {
            this.$message.error('内部错误：' + error);

          }
      )
    }
  },


}
</script>

<style scoped>

</style>