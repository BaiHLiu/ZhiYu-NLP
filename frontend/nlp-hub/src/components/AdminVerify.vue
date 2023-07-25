<template>
  <div>
    <a-row>
      <a-col :span="18">

        <div>
          <a-list item-layout="vertical" size="large" :pagination="pagination" :data-source="listData">
            <a-list-item slot="renderItem" key="item.title" slot-scope="item">

              <a-list-item-meta :description="item.description">
                <a slot="title">{{ item.title }}</a>
                <a-avatar slot="avatar" :src="item.avatar"/>
              </a-list-item-meta>
              <a-tag color="green">
                编号
              </a-tag>
              {{ item.detail_id }}
              <br>

              <a-tag color="blue">
                标题
              </a-tag>
              {{ item.content.title }}

              <br>
              <a-tag color="purple">
                摘要
              </a-tag>
              {{ item.content.summary }}

              <br>
              <br>
              <a-button-group>
                <a-button>取消</a-button>
                <a-button type="primary" @click="admin_pass(item.detail_id)">
                  通过
                </a-button>
              </a-button-group>
            </a-list-item>
          </a-list>
        </div>
      </a-col>

      <a-col :span="6">
        <word-cloud detail_id="0"></word-cloud>
      </a-col>

    </a-row>
  </div>


</template>

<script>
import wordCloud from "@/components/WordCloud";
import axios from "axios";


export default {
  components: {wordCloud},

  beforeCreate: function () {
    this.HOST = process.env.VUE_APP_SERVER_URL;

  },
  mounted() {
    this.get_data();
  },
  data() {
    return {
      listData: undefined,

      pagination: {
        onChange: page => {
          console.log(page);
        },
        pageSize: 3,
      },

    };
  },
  methods: {
    get_data() {
      let new_data = [];

      axios.get(this.HOST + "/get_history", {
        params: {}
      }).then(
          res => {
            let code = res.data['code'];
            let msg = res.data['msg'];

            if (code == 0) {
              let ret = res.data['body'];

              for (let i = ret.length - 1; i >= 0; i--) {
                let info = ret[i];
                // 找出待审核记录
                if (!info[11] == '1') {
                  new_data.push(
                      {
                        title: info[10],
                        avatar: 'https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png',
                        description:
                            '本月已写作**份',
                        content: {
                          summary: info[0],
                          title: info[1]
                        },
                        detail_id: info[6]

                      }
                  )
                }
              }

              this.listData = new_data;
            } else {
              this.$message.error('错误信息：' + msg);
            }

          }
      ).catch(error => {
            this.$message.error('内部错误：' + error);

          }
      )
    },
    admin_pass(sid) {
      axios.get(this.HOST + "/admin_pass", {
        params: {'sid': sid},
        headers: {
          "Authorization": window.localStorage.getItem('token'),
        }
      }).then(
          res => {
            let code = res.data['code'];
            let msg = res.data['msg'];

            if (code == 0) {
              this.$message.success('操作成功！');
              this.get_data();

            } else {
              this.$message.error('错误信息：' + msg);
            }

          }
      ).catch(error => {
            this.$message.error('内部错误：' + error);

          }
      )
    },
  }
}
</script>

<style scoped>

</style>