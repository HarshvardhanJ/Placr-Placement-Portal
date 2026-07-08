import api from "./api";

export const companyApi = {
  async getDashboard() {
    const { data } = await api.get("/company/dashboard");
    return data;
  },

  async getProfile() {
    const { data } = await api.get("/company/profile");
    return data;
  },

  async updateProfile(payload) {
    const { data } = await api.put("/company/profile", payload);
    return data;
  },

  async getDrives() {
    const { data } = await api.get("/company/drives");
    return data;
  },

  async getDriveById(driveId) {
    const { data } = await api.get(`/company/drives/${driveId}`);
    return data;
  },

  async createDrive(payload) {
    const { data } = await api.post("/company/drives", payload);
    return data;
  },

  async updateDrive(driveId, payload) {
    const { data } = await api.put(`/company/drives/${driveId}`, payload);
    return data;
  },

  async closeDrive(driveId) {
    const { data } = await api.put(`/company/drives/${driveId}/close`);
    return data;
  },

  async getDriveApplications(driveId) {
    const { data } = await api.get(`/company/drives/${driveId}/applications`);
    return data;
  },

  async updateApplicationStatus(driveId, applicationId, payload) {
    const { data } = await api.put(
      `/company/drives/${driveId}/applications/${applicationId}`,
      payload,
    );
    return data;
  },

  async getInterviews() {
    const { data } = await api.get("/company/interviews");
    return data;
  },

  async getPlacements() {
    const { data } = await api.get("/company/placements");
    return data;
  },

  async updatePlacement(placementId, payload) {
    const { data } = await api.put(
      `/company/placements/${placementId}`,
      payload,
    );
    return data;
  },

  async uploadOfferLetter(placementId, file) {
    const formData = new FormData();
    formData.append("offer_letter", file);

    const { data } = await api.post(
      `/company/placements/${placementId}/offer-letter`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      },
    );

    return data;
  },

  async startExport() {
    const { data } = await api.post("/company/exports");
    return data;
  },

  async getExportStatus(taskId) {
    const { data } = await api.get(`/company/exports/status/${taskId}`);
    return data;
  },

  async downloadExport(filename) {
    return api.get(`/company/exports/download/${filename}`, {
      responseType: "blob",
    });
  },
};

export default companyApi;
