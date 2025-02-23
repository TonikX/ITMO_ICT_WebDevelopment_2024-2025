<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" v-model="valid" @submit.prevent="login">
              <v-text-field
                v-model="username"
                label="Username"
                type="text"
                required
                outlined
                prepend-icon="mdi-account"
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Password"
                type="password"
                required
                outlined
                prepend-icon="mdi-lock"
              ></v-text-field>
              <v-btn
                type="submit"
                color="primary"
                block
                class="mt-4"
                :disabled="!valid"
              >
                Login
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <Loading v-if="isLoading" />
  </v-container>
</template>

<script>
import { mapActions } from "vuex";
import Loading from "@/components/Loading.vue";

export default {
  name: "Login",
  components: {
    Loading,
  },
  data() {
    return {
      valid: false,
      username: "",
      password: "",
      isLoading: false,
    };
  },
  methods: {
    ...mapActions("auth", ["login"]),
    async login() {
      if (this.$refs.form.validate()) {
        try {
          this.isLoading = true;
          const success = await this.login({
            username: this.username,
            password: this.password,
          });
          if (success) {
            this.$router.push("/");
          } else {
            alert("Invalid username or password");
          }
        } catch (error) {
          console.error(error);
          alert("Login failed");
        } finally {
          this.isLoading = false;
        }
      }
    },
  },
};
</script>
