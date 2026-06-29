import api from "./api";

export const studentApi = {
  async getDashboard() {
    const { data } = await api.get("/student/dashboard");
    return data;
  },

  async getProfile() {
    const { data } = await api.get("/student/profile");
    return data;
  },

  async updateProfile(payload) {
    const { data } = await api.put("/student/profile", payload);
    return data;
  },

  async uploadResume(file) {
    const formData = new FormData();
    formData.append("resume", file);

    const { data } = await api.post("/student/profile/resume", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return data;
  },


  async downloadResume() {
    return api.get("/student/profile/resume", {
      responseType: "blob",
    });
  },

  async getDrives(search = "") {
    const { data } = await api.get("/student/drives", {
      params: search ? { search } : undefined,
    });
    return data;
  },

  async getDriveById(driveId) {
    const { data } = await api.get(`/student/drives/${driveId}`);
    return data;
  },

  async applyToDrive(driveId) {
    const { data } = await api.post(`/student/drives/${driveId}/apply`);
    return data;
  },

  async getApplications() {
    const { data } = await api.get("/student/applications");
    return data;
  },

  async getPlacements() {
    const { data } = await api.get("/student/placements");
    return data;
  },

  async getPlacementById(placementId) {
    const { data } = await api.get(`/student/placements/${placementId}`);
    return data;
  },

  async downloadOfferLetter(placementId) {
    return api.get(`/student/placements/${placementId}/offer-letter`, {
      responseType: "blob",
    });
  },
};

export default studentApi;
