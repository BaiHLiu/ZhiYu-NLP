<template>
  <div>
    <a-input v-model="username" placeholder="用户名"/>
    <a-input v-model="email" placeholder="E-Mail"/>
    <a-input v-model="password" placeholder="密码"/>
    <a-input v-model="auth" placeholder="认证码"/>
    <a-button type="primary" @click="register">注册</a-button>
  </div>
</template>

<script>

import axios from "axios";

export default {
  name: "UserRegister",
  data() {
    return {
      email: '',
      password: '',
      auth: '',
      username: ''
    }
  },
  beforeCreate() {
    this.HOST = process.env.VUE_APP_SERVER_URL;
  },
  methods: {
    register() {
      let formData = new FormData();
      formData.append('email', this.email);
      formData.append('password', this.password);
      formData.append('auth', this.auth);
      formData.append('username', this.username);

      axios.post(this.HOST + "/user_register", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }).then(
          res => {
            let code = res.data['code'];
            let msg = res.data['msg'];

            if (code == 0) {
              this.$message.success('注册成功！请返回登录');

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