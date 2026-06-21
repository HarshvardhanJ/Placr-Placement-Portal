import api from "api";

export const getApplications = () => {
  return api.get("/admin/applications");
};

export const getCompanies = () => {
  return api.get("/admin/companies");
};

export const getStudents = () => {
  return api.get("/admin/students");
};

export const getDrives = () => {
  return api.get("/admin/drives");
};
