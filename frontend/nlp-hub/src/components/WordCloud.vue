<template>
  <div id="echartsWordcloud" style="width:400px;height:400px; margin-top: -20px"></div>
</template>


<script>
import * as echarts from 'echarts';
import axios from "axios";

require('echarts-wordcloud');


export default {
  props: ['detail_id'],
  beforeCreate() {
    this.HOST = process.env.VUE_APP_SERVER_URL;

  },
  created() {
    this.getWordCloud(this.detail_id);
  },
  mounted() {


  },
  data() {
    return {
      worddata: []
    }
  },
  methods: {
    getWordCloud(id) {
      axios.get(this.HOST + "/get_cloud", {
        params: {id: id}
      }).then(
          res => {
            let code = res.data['code'];
            let msg = res.data['msg'];

            if (code == 0) {
              let wc = res.data['body'];
              for (let i = 0; i < wc.length; i++) {
                this.worddata.push(
                    {
                      name: wc[i][0],
                      value: wc[i][1],
                    }
                )
              }

              this.initEcharts();

            } else {
              this.$message.error('错误信息：' + msg);
            }

          }
      ).catch(error => {
            this.$message.error('内部错误：' + error);

          }
      )
    },
    initEcharts() {
      let echartsWordcloud = echarts.init(document.getElementById("echartsWordcloud"));
      let option = {
        title: {
          text: "",
          x: "center"
        },
        series: [
          {
            type: "wordCloud",
            //用来调整词之间的距离
            gridSize: 12,
            //用来调整字的大小范围
            sizeRange: [18, 38],
            rotationRange: [1, 30],
            //随机生成字体颜色
            textStyle: {

              color: function () {
                var colors = ['#fda67e', '#81cacc', '#cca8ba', "#88cc81", "#82a0c5", '#fddb7e', '#735ba1', '#bda29a', '#6e7074', '#546570', '#c4ccd3'];
                return colors[parseInt(Math.random() * 10)];
              }


            },
            //位置相关设置
            // left: "center",
            // top: "center",
            // right: null,
            // bottom: null,
            // width: "300%",
            // height: "300%",
            //数据
            data: this.worddata
          }
        ]
      };
      echartsWordcloud.setOption(option);
      //点击事件
      echartsWordcloud.on("click", function () {
      })
    }
  }
}
</script>