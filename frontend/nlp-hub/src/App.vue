<template>
  <a-layout id="components-layout-demo-side" style="min-height: 100vh">
    <a-layout-sider v-model="collapsed" collapsible>
      <div class="logo" style="margin-bottom: 30px">
        <img src="/logo-dark.png" height="48px">
      </div>
      <a-menu theme="dark" :default-selected-keys="['1']" mode="inline">
        <a-menu-item key="1">
          <a-icon type="form"/>
          标题摘要生成
          <router-link to='/summary_generate'></router-link>
        </a-menu-item>

        <a-menu-item key="2">
          <a-icon type="login"/>
          批量生成
          <router-link to='/batch_generate'></router-link>
        </a-menu-item>

        <a-menu-item key="3">
          <a-icon type="clock-circle"/>
          处理记录
          <router-link to='/history_list'></router-link>
        </a-menu-item>

        <a-menu-item key="4" v-if="userinfo && userinfo['isAdmin']==1">
          <a-icon type="setting"/>
          管理后台 &nbsp;
          <a-badge :count="statistics.unverify"/>
          <router-link to='/verify'></router-link>
        </a-menu-item>

      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0;">


        <!--        登录框-->
        <div v-if="! isLogin" style="text-align: right; padding-top: 10px; padding-right: 20px">
          <a-form-model layout="inline" :model="formInline" @submit="handleLogin" @submit.native.prevent>
            <a-form-model-item>
              <a-input v-model="formInline.email" placeholder="E-Mail">
                <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)"/>
              </a-input>
            </a-form-model-item>
            <a-form-model-item>
              <a-input v-model="formInline.password" type="password" placeholder="密码">
                <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)"/>
              </a-input>
            </a-form-model-item>
            <a-form-model-item>
              <a-button
                  type="primary"
                  html-type="submit"
                  :disabled="formInline.user === '' || formInline.password === ''"
              >
                登录
              </a-button>
              <a-button @click="showModal">
                注册
              </a-button>
            </a-form-model-item>
          </a-form-model>

          <a-modal
              title="注册用户"
              :visible="modal.visible"
              @ok="handleModalCancel"
              @cancel="handleModalCancel"
          >
            <user-register></user-register>
          </a-modal>


        </div>

        <!--        已登录显示-->
        <div v-if="isLogin" style="text-align: right; padding-top: 10px; margin-right: 100px">
          <a-avatar icon="user"/>
          {{ userinfo.username }}
          &nbsp;&nbsp;
          <a-button @click="handleLogout">
            退出
          </a-button>
        </div>

      </a-layout-header>
      <a-layout-content style="margin: 0 16px">
        <a-breadcrumb style="margin: 16px 0">
          <a-breadcrumb-item></a-breadcrumb-item>
        </a-breadcrumb>
        <div :style="{ padding: '24px', background: '#fff', minHeight: '360px' }">
          <router-view></router-view>
        </div>
      </a-layout-content>
      <a-layout-footer style="text-align: center">
         ©2022 知行合一NLP研发组 <br>版权所有
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script>
import axios from "axios";
import UserRegister from "@/components/UserRegister";

export default {
  components: {UserRegister},
  data() {
    return {
      collapsed: false,
      formInline: {
        email: '',
        password: '',
      },
      isLogin: false,
      userinfo: undefined,

      statistics: {
        unverify: 0
      },

      modal: {
        visible: false,
        confirmLoading: false
      },
    };
  },
  beforeCreate() {
    this.HOST = process.env.VUE_APP_SERVER_URL;
  },
  mounted() {
    this.checkLogin();
    this.getStatus();

  },
  methods: {
    handleLogin() {
      let formData = new FormData();
      formData.append('email', this.formInline.email);
      formData.append('password', this.formInline.password);
      this.isLogin = true;

      axios.post(this.HOST + "/user_login", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }).then(
          res => {
            let code = res.data['code'];
            let msg = res.data['msg'];

            if (code == 0) {
              this.$message.success('欢迎您：' + res.data['body']['userinfo']['username']);
              window.localStorage.setItem('userinfo', JSON.stringify(res.data['body']['userinfo']));
              window.localStorage.setItem('token', res.data['body']['token']);

              window.location.reload();

            } else {
              this.$message.error('错误信息：' + msg);
            }

          }
      ).catch(error => {
            this.$message.error('网络错误：' + error);

          }
      )
    },
    handleLogout() {
      window.localStorage.clear();
      this.isLogin = false;
      this.$message.success('退出成功！');
    },
    checkLogin() {
      //检查登录态
      let userinfo = window.localStorage.getItem('userinfo');
      if (userinfo) {
        this.isLogin = true;
        this.userinfo = JSON.parse(window.localStorage.getItem('userinfo'));
      } else {
        this.$notification.open({
          message: '当前未登录',
          description:
              '未登录时，您仍可以用游客身份浏览，但无法使用生成、管理等功能。',
          icon: <a-icon type="smile" style="color: #108ee9"/>,
        });
      }
    },
    getStatus() {
      axios.get(this.HOST + "/status", {}).then(
          res => {
            console.log(res.data);
            this.statistics.unverify = res.data['body']['today_unverify'];

          }
      )

    },
    showModal() {
      this.modal.visible = true;
    },
    handleModalCancel(){
      this.modal.visible = false;
    }
  },

};
</script>

<style>
#components-layout-demo-side .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px;
}

</style>
