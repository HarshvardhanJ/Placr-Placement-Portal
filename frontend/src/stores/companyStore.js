import { defineStore } from "pinia";
import companyApi from "@/services/companyApi";

const defaultDashboard = {
  company: null,
  stats: {
    active_drives: 0,
    total_applications: 0,
    interviews_scheduled: 0,
    offers_made: 0,
  },
  trends: {
    active_drives_new_7d: 0,
    total_applications_new_7d: 0,
  },
  active_drives: [],
  recent_applicants: [],
};

export const useCompanyStore = defineStore("company", {
  state: () => ({
    dashboard: { ...defaultDashboard },
    drives: [],
    interviews: [],
    placements: [],
    loadingDashboard: false,
    loadingDrives: false,
    loadingInterviews: false,
    loadingPlacements: false,
    error: null,
    pendingApproval: false,
    profile: null,
    selectedDrive: null,
    selectedApplications: [],
    selectedInterviews: [],
    selectedPlacement: null,
  }),

  getters: {
    company(state) {
      return state.dashboard.company || state.profile;
    },

    statsCards(state) {
      const stats = state.dashboard.stats;
      const trends = state.dashboard.trends;
      return [
        {
          key: "active_drives",
          label: "Active Drives",
          value: stats.active_drives,
          icon: "ti-briefcase",
          delta: trends.active_drives_new_7d
            ? `+${trends.active_drives_new_7d} this week`
            : "",
        },
        {
          key: "total_applications",
          label: "Total Applications",
          value: stats.total_applications,
          icon: "ti-inbox",
          delta: trends.total_applications_new_7d
            ? `+${trends.total_applications_new_7d}`
            : "",
        },
        {
          key: "interviews_scheduled",
          label: "Interviews Scheduled",
          value: stats.interviews_scheduled,
          icon: "ti-calendar-event",
        },
        {
          key: "offers_made",
          label: "Offers Made",
          value: stats.offers_made,
          icon: "ti-award",
        },
      ];
    },

    activeDrives(state) {
      return state.dashboard.active_drives;
    },

    recentApplicants(state) {
      return state.dashboard.recent_applicants;
    },

    placementStats(state) {
      const placements = state.placements || [];
      const today = new Date();
      const nextSevenDays = new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000);

      const joiningSoon = placements.filter((placement) => {
        if (!placement.joining_date) return false;
        const d = new Date(placement.joining_date);
        return !Number.isNaN(d.getTime()) && d >= today && d <= nextSevenDays;
      }).length;

      const withOfferLetter = placements.filter(
        (placement) => placement.offer_letter_uploaded,
      ).length;

      const averageSalary = placements.length
        ? Math.round(
            placements.reduce(
              (sum, placement) => sum + Number(placement.salary || 0),
              0,
            ) / placements.length,
          )
        : 0;

      return [
        {
          key: "placements_total",
          label: "Placements",
          value: placements.length,
          icon: "ti-trophy",
        },
        {
          key: "joining_soon",
          label: "Joining Soon",
          value: joiningSoon,
          icon: "ti-calendar",
        },
        {
          key: "offer_letters",
          label: "Offer Letters",
          value: withOfferLetter,
          icon: "ti-file-text",
        },
        {
          key: "average_salary",
          label: "Avg Salary",
          value: averageSalary
            ? `₹${averageSalary.toLocaleString("en-IN")}`
            : "—",
          icon: "ti-currency-rupee",
        },
      ];
    },
  },

  actions: {
    async fetchDashboard(force = false) {
      if (this.loadingDashboard && !force) return;
      this.loadingDashboard = true;
      this.error = null;
      this.pendingApproval = false;

      try {
        const data = await companyApi.getDashboard();
        this.dashboard = {
          ...defaultDashboard,
          ...data,
          stats: { ...defaultDashboard.stats, ...(data.stats || {}) },
          trends: { ...defaultDashboard.trends, ...(data.trends || {}) },
        };
        this.profile = data.company || this.profile;
      } catch (error) {
        if (error?.response?.status === 403) {
          this.pendingApproval = true;
        }
        this.error =
          error?.response?.data?.error ||
          error?.message ||
          "Failed to load company dashboard";
      } finally {
        this.loadingDashboard = false;
      }
    },

    async fetchProfile() {
      this.error = null;
      try {
        const data = await companyApi.getProfile();
        this.profile = data;
        return data;
      } catch (error) {
        this.error =
          error?.response?.data?.error || "Failed to load company profile";
        throw error;
      }
    },

    async updateProfile(payload) {
      const data = await companyApi.updateProfile(payload);
      this.profile = data.company || data;
      if (this.dashboard.company) {
        this.dashboard.company = this.profile;
      }
      return data;
    },

    async fetchDrives(force = false) {
      if (this.loadingDrives && !force) return this.drives;
      this.loadingDrives = true;
      this.error = null;
      try {
        const data = await companyApi.getDrives();
        this.drives = data.drives || [];
        return this.drives;
      } catch (error) {
        this.error = error?.response?.data?.error || "Failed to load drives";
        throw error;
      } finally {
        this.loadingDrives = false;
      }
    },

    async fetchDriveById(driveId) {
      this.error = null;
      const data = await companyApi.getDriveById(driveId);
      this.selectedDrive = data;
      return data;
    },

    async fetchDriveApplications(driveId) {
      this.error = null;
      const data = await companyApi.getDriveApplications(driveId);
      this.selectedApplications = data.applications || [];
      return data;
    },

    async createDrive(payload) {
      const data = await companyApi.createDrive(payload);
      await this.fetchDrives(true);
      return data;
    },

    async updateDrive(driveId, payload) {
      const data = await companyApi.updateDrive(driveId, payload);
      await this.fetchDrives(true);
      return data;
    },

    async closeDrive(driveId) {
      const data = await companyApi.closeDrive(driveId);
      await this.fetchDrives(true);
      return data;
    },

    async updateApplicationStatus(driveId, applicationId, payload) {
      const data = await companyApi.updateApplicationStatus(
        driveId,
        applicationId,
        payload,
      );
      return data;
    },

    async fetchInterviews(force = false) {
      if (this.loadingInterviews && !force) return this.interviews;
      this.loadingInterviews = true;
      this.error = null;
      try {
        const data = await companyApi.getInterviews();
        this.interviews = data.interviews || [];
        return this.interviews;
      } catch (error) {
        this.error =
          error?.response?.data?.error || "Failed to load interviews";
        throw error;
      } finally {
        this.loadingInterviews = false;
      }
    },

    async fetchPlacements(force = false) {
      if (this.loadingPlacements && !force) return this.placements;
      this.loadingPlacements = true;
      this.error = null;
      try {
        const data = await companyApi.getPlacements();
        this.placements = data.placements || [];
        return this.placements;
      } catch (error) {
        this.error =
          error?.response?.data?.error || "Failed to load placements";
        throw error;
      } finally {
        this.loadingPlacements = false;
      }
    },

    async updatePlacement(placementId, payload) {
      const data = await companyApi.updatePlacement(placementId, payload);
      await this.fetchPlacements(true);
      return data;
    },

    async uploadOfferLetter(placementId, file) {
      const data = await companyApi.uploadOfferLetter(placementId, file);
      await this.fetchPlacements(true);
      return data;
    },

    clearCompanyState() {
      this.dashboard = { ...defaultDashboard };
      this.drives = [];
      this.interviews = [];
      this.placements = [];
      this.loadingDashboard = false;
      this.loadingDrives = false;
      this.loadingInterviews = false;
      this.loadingPlacements = false;
      this.error = null;
      this.pendingApproval = false;
      this.profile = null;
      this.selectedDrive = null;
      this.selectedApplications = [];
      this.selectedInterviews = [];
      this.selectedPlacement = null;
    },
  },
});

export default useCompanyStore;
