<template>
  <v-container fluid class="login-page">
    <v-row justify="center" align="center">
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title class="text-h5 justify-center">
            Login to Your To-Do List
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-text-field v-model="user" :rules="emailRules" label="Username" required></v-text-field>
              <v-text-field v-model="password" :rules="passwordRules" label="Password" type="password"
                required></v-text-field>
              <v-btn :disabled="!valid" color="primary" @click="login">
                Login
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'; 
export default defineComponent({
  name: 'Login',
  setup() {
    const user = ref('');
    const password = ref('');
    const valid = ref(false);
    const router = useRouter(); // Get the router instance

    const emailRules : any = [
      (v: string) => !!v || 'Email is required',
      // (v: string) => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    ];

    const passwordRules = [(v: string) => !!v || 'Password is required'];

    const login = async () => {
      try {

        // Add your login logic here
        console.log('Logging in with:', user.value, password.value);
        let req = await fetch("http://localhost:3030/login", {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username: user.value, password: password.value })
        })
        interface LoginData {
          msg: string;
          user?: string;
          error? : string;
        }
        let data : LoginData = await req.json()
        console.log(data)
        if(data.msg == "good" ){
          // Redirect to dashboard page
          router.push('/home');
        }
      } catch (error) {
        console.log(error.message)
      }
    };

    return {
      user,
      password,
      valid,
      emailRules,
      passwordRules,
      login,
    };
  },
});
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.v-card {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
