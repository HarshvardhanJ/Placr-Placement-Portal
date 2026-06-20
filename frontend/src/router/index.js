import { createRouter, createWebHistory } from "vue-router";

import LoginView from "@/views/auth/LoginView.vue";
import StudentRegisterView from "@/views/auth/StudentRegisterView.vue";
import CompanyRegisterView from "@/views/auth/CompanyRegisterView.vue";
import LandingView from "@/views/auth/LandingView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";
import AdminDashboardView from "@/views/admin/DashboardView.vue";
import AdminCompaniesView from "@/views/admin/CompaniesView.vue";
import AdminStudentsView from "@/views/admin/StudentsView.vue";
import AdminDrivesView from "@/views/admin/DrivesView.vue";
import AdminApplicationsView from "@/views/admin/ApplicationsView.vue";
// import CompanyDashboardView from "@/views/company/DashboardView.vue";
// import StudentDashboardView from "@/views/student/DashboardView.vue";

const routes = [
  {
    path: "/",
    name: "landing",
    component: LandingView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
  },
  {
    path: "/register/student",
    name: "student-register",
    component: StudentRegisterView,
  },
  {
    path: "/register/company",
    name: "company-register",
    component: CompanyRegisterView,
  },
  {
    path: "/admin",
    name: "admin-dashboard",
    component: AdminDashboardView,
  },
  {
    path: "/admin/companies",
    name: "admin-company-dashboard",
    component: AdminCompaniesView,
  },
  {
    path: "/admin/students",
    name: "admin-student-dashboard",
    component: AdminStudentsView,
  },
  {
    path: "/admin/drives",
    name: "admin-drives-dashboard",
    component: AdminDrivesView,
  },
  {
    path: "/admin/applications",
    name: "admin-application-dashboard",
    component: AdminApplicationsView,
  },
  // {
  //   path: "/company",
  //   name: "company-dashboard",
  //   component: CompanyDashboardView,
  // },
  // {
  //   path: "/student",
  //   name: "student-dashboard",
  //   component: StudentDashboardView,
  // },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
