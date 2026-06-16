import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    user: localStorage.getItem("user") || null,
  }),
  actions: {
    login(token, user) {
      this.token = token;
      this.user = user;

      localStorage.setItem("token", token);
      localStorage.setItem("user", user);
    },
    logout() {
      this.token = null;
      this.user = null;

      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },
  },
});
