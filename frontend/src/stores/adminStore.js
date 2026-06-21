import { defineStore } from "pinia";
import api from "@/services/api";

export const useAdminStore = defineStore("admin", {
  state: () => ({
    stats: {
      students: 0,
      companies: 0,
      drives: 0,
      applications: 0,
      pending_companies: 0,
      pending_drives: 0,
      blacklisted: 0,
    },
  }),

  actions: {
    async fetchDashboardStats() {
      const response = await api.get("/admin/dashboard");
      this.stats = response.data.stats;
    },
  },
});

export default useAdminStore;
