<template>

  <div>
    <a-drawer
        title="详细信息"
        placement="right"
        closable
        :visible="detail_visible"
        @close="onClose"
        width=900px
    >
      <div v-if="detail_visible">
        <detail-page :detail_id="detail_id"></detail-page>
        <word-cloud :detail_id="detail_id"></word-cloud>
      </div>
    </a-drawer>

    <a-table :data-source="data" :columns="columns" :loading="loading">
      <span slot="tags" slot-scope="tags">
      <a-tag
          v-for="tag in tags"
          :key="tag"
          :color="(tag == '待审核' || tag=='排队中')? 'orange' : 'green'"
      >
        {{ tag }}
      </a-tag>
      </span>

      <span slot="item_id" slot-scope="item_id">
        <a @click="showDraft(item_id)">详情</a>
      </span>

      <div
          slot="filterDropdown"
          slot-scope="{ setSelectedKeys, selectedKeys, confirm, clearFilters, column }"
          style="padding: 8px"
      >
        <a-input
            v-ant-ref="c => (searchInput = c)"
            :placeholder="`Search ${column.dataIndex}`"
            :value="selectedKeys[0]"
            style="width: 188px; margin-bottom: 8px; display: block;"
            @change="e => setSelectedKeys(e.target.value ? [e.target.value] : [])"
            @pressEnter="() => handleSearch(selectedKeys, confirm, column.dataIndex)"
        />
        <a-button
            type="primary"
            icon="search"
            size="small"
            style="width: 90px; margin-right: 8px"
            @click="() => handleSearch(selectedKeys, confirm, column.dataIndex)"
        >
          搜索
        </a-button>
        <a-button size="small" style="width: 90px" @click="() => handleReset(clearFilters)">
          重置
        </a-button>
      </div>
      <a-icon
          slot="filterIcon"
          slot-scope="filtered"
          type="search"
          :style="{ color: filtered ? '#108ee9' : undefined }"
      />
      <template slot="customRender" slot-scope="text, record, index, column">

        <span v-if="searchText && searchedColumn === column.dataIndex">
        <template
            v-for="(fragment, i) in text
            .toString()
            .split(new RegExp(`(?<=${searchText})|(?=${searchText})`, 'i'))"
        >
          <mark
              v-if="fragment.toLowerCase() === searchText.toLowerCase()"
              :key="i"
              class="highlight"
          >{{ fragment }}</mark
          >
          <template v-else>{{ fragment }}</template>
        </template>
      </span>

        <template v-else>
          {{ text }}
        </template>
      </template>


    </a-table>


  </div>
</template>

<script>

import axios from "axios";
import DetailPage from "@/components/DetailPage";
import WordCloud from "@/components/WordCloud";

export default {

  name: "HistoryList",
  components: {DetailPage, WordCloud},
  props: ['hide_time_use'],
  beforeCreate() {
    this.HOST = process.env.VUE_APP_SERVER_URL;

  },
  mounted() {
    this.get_table_data();
    this.timer = setInterval(this.get_table_data, 4000);

    if (this.hide_time_use)
      this.columns[2] = {};
      this.columns[4] = {};

  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  data() {
    return {
      data: [],
      searchText: '',
      searchInput: null,
      searchedColumn: '',
      detail_visible: false,

      status_text: '准备开始',
      status_icon: 'default',
      user_rate: '',
      original_words: '',
      summary_words: '',
      title_words: '',
      title: '',
      summary: '',
      file_name: '',
      user_name: '',
      contents: '',
      loading: true,
      item_id: 0,
      detail_id: 0,

      columns: [

        {
          title: '状态',
          dataIndex: 'tags',
          key: 'tags',
          scopedSlots: {
            customRender: 'tags',
          },
        },
        {
          title: '标题',
          dataIndex: 'title',
          key: 'title',
          scopedSlots: {
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon',
            customRender: 'customRender',
          },
          onFilter: (value, record) =>
              record.title
                  .toString()
                  .toLowerCase()
                  .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: visible => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              }, 0);
            }
          },
        },

        {
          title: '评分',
          dataIndex: 'user_rate',
          key: 'user_rate',
          scopedSlots: {},

        },
        {
          title: '提交人',
          dataIndex: 'user_name',
          key: 'user_name',
          scopedSlots: {
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon',
            customRender: 'customRender',
          },
          onFilter: (value, record) =>
              record.title
                  .toString()
                  .toLowerCase()
                  .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: visible => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              }, 0);
            }
          },
        },
        {
          title: '文件名',
          dataIndex: 'file',
          key: 'file',
          ellipsis: true,
          scopedSlots: {
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon',
            customRender: 'customRender',
          },
          onFilter: (value, record) =>
              record.user_rate
                  .toString()
                  .toLowerCase()
                  .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: visible => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: '提交时间',
          dataIndex: 'submit_time',
          key: 'submit_time',
          scopedSlots: {
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon',
            customRender: 'customRender',
          },
          onFilter: (value, record) =>
              record.submit_time
                  .toString()
                  .toLowerCase()
                  .includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: visible => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus();
              });
            }
          },
        },
        {
          title: '操作',
          dataIndex: 'item_id',
          key: 'item_id',
          width: 150,
          scopedSlots: {
            customRender: 'item_id',
          },


        },
      ],
    };
  },
  methods: {
    handleSearch(selectedKeys, confirm, dataIndex) {
      confirm();
      this.searchText = selectedKeys[0];
      this.searchedColumn = dataIndex;
    },

    handleReset(clearFilters) {
      clearFilters();
      this.searchText = '';
    },


    onClose() {
      this.detail_visible = false;
      this.get_table_data();
    },

    get_table_data() {

      this.loading = true;

      let new_data = [];
      axios.get(this.HOST + "/get_history", {
        params: {}
      }).then(
          res => {
            let code = res.data['code'];
            let msg = res.data['msg'];

            if (code == 0) {
              //处理数据逻辑

              this.loading = false;

              let ret = res.data['body'];

              for (let i = ret.length - 1; i >= 0; i--) {
                let verify_tag = '待审核';

                if(ret[i][11] == '1'){
                  verify_tag = '审核通过';
                }
                let rowData = {
                  key: i.toString(),
                  title: ret[i][1],
                  user_rate: ret[i][9],
                  file: ret[i][3],
                  submit_time: ret[i][4],
                  tags: ['已生成',verify_tag],
                  item_id: ret[i][6],
                  user_name: ret[i][10]
                };


                if (ret[i][5] == -1)
                  rowData['tags'] = ['失败'];
                else if(ret[i][5] == 0)
                  rowData['tags'] = ['排队中'];

                new_data.push(rowData);
                this.data = new_data;
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
    showDraft(item_id) {
      this.detail_id = item_id;
      this.detail_visible = true;

    }

  },

}


</script>

<style scoped>
.highlight {
  background-color: rgb(255, 192, 105);
  padding: 0px;
}
</style>