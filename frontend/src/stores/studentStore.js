import { defineStore } from "pinia";
import studentApi from "@/services/studentApi";

const defaultDashboard = {
  counts: {
    eligible: 0,
    applied: 0,
    shortlisted: 0,
    selected: 0,
  },
  eligible_drives: [],
  applied_drives: [],
  shortlisted_drives: [],
  selected_drives: [],
  upcoming_interviews: [],
};

export const useStudentStore = defineStore("student", {
  state: () => ({
    dashboard: { ...defaultDashboard },
    profile: null,
    drives: [],
    applications: [],
    placements: [],
    loadingDashboard: false,
    loadingProfile: false,
    loadingDrives: false,
    loadingApplications: false,
    loadingPlacements: false,
    error: null,
    profileWarning: false,
  }),

  getters: {
    student(state) {
      return state.profile || state.dashboard?.student || null;
    },

    studentName(state) {
      return state.profile?.name || state.dashboard?.student?.name || "Student";
    },

    studentInitials(state) {
      const name =
        state.profile?.name || state.dashboard?.student?.name || "ST";
      return (
        name
          .split(" ")
          .filter(Boolean)
          .slice(0, 2)
          .map((part) => part[0]?.toUpperCase())
          .join("") || "ST"
      );
    },

    hasResume(state) {
      return Boolean(
        state.profile?.resume_path ||
        state.profile?.resume_url ||
        state.profile?.resume,
      );
    },

    statsCards(state) {
      const counts = state.dashboard?.counts || defaultDashboard.counts;

      return [
        {
          key: "eligible",
          label: "Eligible Drives",
          value: counts.eligible,
          icon: "ti-briefcase",
          delta: "Recommended for you",
        },
        {
          key: "applied",
          label: "Applications Submitted",
          value: counts.applied,
          icon: "ti-send",
          delta: "Across all drives",
        },
        {
          key: "shortlisted",
          label: "Shortlisted",
          value: counts.shortlisted,
          icon: "ti-star",
          delta: "Waiting on interviews",
        },
        {
          key: "selected",
          label: "Placements",
          value: counts.selected,
          icon: "ti-trophy",
          delta: "Offers received",
        },
      ];
    },

    reportCards(state) {
      const resumeUploaded = Boolean(
        state.profile?.resume_path ||
        state.profile?.resume_url ||
        state.profile?.resume,
      );
      const applications = state.dashboard?.counts?.applied || 0;
      const placements = state.dashboard?.counts?.selected || 0;

      return [
        {
          key: "resume",
          label: "Resume",
          value: resumeUploaded ? "Uploaded" : "Missing",
          caption: resumeUploaded
            ? "Ready for applications"
            : "Upload your resume PDF",
          icon: "ti-file-description",
        },
        {
          key: "applications",
          label: "Applications",
          value: applications,
          caption: "Tracked in your dashboard",
          icon: "ti-send",
        },
        {
          key: "placements",
          label: "Placements",
          value: placements,
          caption: "Offers or confirmations",
          icon: "ti-trophy",
        },
      ];
    },

    eligibleDrives(state) {
      return state.dashboard?.eligible_drives || [];
    },

    appliedDrives(state) {
      return state.dashboard?.applied_drives || [];
    },

    shortlistedDrives(state) {
      return state.dashboard?.shortlisted_drives || [];
    },

    selectedDrives(state) {
      return state.dashboard?.selected_drives || [];
    },

    upcomingInterviews(state) {
      return state.dashboard?.upcoming_interviews || [];
    },

    analyticsSummary(state) {
      const counts = state.dashboard?.counts || defaultDashboard.counts;
      return {
        eligible: counts.eligible || 0,
        applied: counts.applied || 0,
        shortlisted: counts.shortlisted || 0,
        selected: counts.selected || 0,
      };
    },

    applicationTabs(state) {
      const applied = state.dashboard?.applied_drives || [];
      const shortlisted = state.dashboard?.shortlisted_drives || [];
      const selected = state.dashboard?.selected_drives || [];

      return {
        all: applied.length + shortlisted.length + selected.length,
        applied: applied.length,
        shortlisted: shortlisted.length,
        selected: selected.length,
      };
    },

    profileComplete(state) {
      return Boolean(
        state.profile?.department && state.profile?.cgpa && state.profile?.year,
      );
    },
  },

  actions: {
    clearStudentState() {
      this.dashboard = { ...defaultDashboard };
      this.profile = null;
      this.drives = [];
      this.applications = [];
      this.placements = [];
      this.error = null;
      this.profileWarning = false;
    },

    async fetchDashboard(force = false) {
      if (this.loadingDashboard && !force) return;

      this.loadingDashboard = true;
      this.error = null;
      this.profileWarning = false;

      try {
        const data = await studentApi.getDashboard();
        this.dashboard = {
          ...defaultDashboard,
          ...data,
          counts: { ...defaultDashboard.counts, ...(data.counts || {}) },
        };
        return data;
      } catch (error) {
        const message =
          error?.response?.data?.error ||
          error?.message ||
          "Failed to load student dashboard";

        if (error?.response?.status === 400) {
          this.profileWarning = true;
        } else {
          this.error = message;
        }

        throw error;
      } finally {
        this.loadingDashboard = false;
      }
    },

    async fetchProfile() {
      if (this.loadingProfile) return this.profile;

      this.loadingProfile = true;
      this.error = null;

      try {
        const data = await studentApi.getProfile();
        this.profile = data;
        return data;
      } catch (error) {
        this.error =
          error?.response?.data?.error || "Failed to load student profile";
        throw error;
      } finally {
        this.loadingProfile = false;
      }
    },

    async refreshStudentState() {
      await Promise.allSettled([this.fetchProfile(), this.fetchDashboard()]);
    },

    async updateProfile(payload) {
      const data = await studentApi.updateProfile(payload);
      this.profile = data.student || data;
      return data;
    },

    async uploadResume(file) {
      const data = await studentApi.uploadResume(file);
      if (this.profile) {
        this.profile.resume_path = data.resume_path;
      }
      return data;
    },

    async fetchDrives(search = "") {
      this.loadingDrives = true;
      this.error = null;

      try {
        const data = await studentApi.getDrives(search);
        this.drives = data.drives || [];
        return data;
      } catch (error) {
        this.error =
          error?.response?.data?.error || "Failed to load available drives";
        throw error;
      } finally {
        this.loadingDrives = false;
      }
    },

    async fetchApplications() {
      this.loadingApplications = true;
      this.error = null;

      try {
        const data = await studentApi.getApplications();
        this.applications = data.applications || [];
        return data;
      } catch (error) {
        this.error =
          error?.response?.data?.error || "Failed to load applications";
        throw error;
      } finally {
        this.loadingApplications = false;
      }
    },

    async fetchPlacements() {
      this.loadingPlacements = true;
      this.error = null;

      try {
        const data = await studentApi.getPlacements();
        this.placements = data.placements || [];
        return data;
      } catch (error) {
        this.error =
          error?.response?.data?.error || "Failed to load placements";
        throw error;
      } finally {
        this.loadingPlacements = false;
      }
    },
  },
});

export default useStudentStore;
