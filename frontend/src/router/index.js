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
import AdminAnalyticsView from "@/views/admin/AnalyticsView.vue";
import AdminReportsView from "@/views/admin/ReportsView.vue";
import CompanyDashboardView from "@/views/company/DashboardView.vue";
import CompanyDrivesView from "@/views/company/DrivesView.vue";
import CompanyApplicationsView from "@/views/company/ApplicationsView.vue";
import CompanyInterviewsView from "@/views/company/InterviewsView.vue";
import CompanyProfileView from "@/views/company/ProfileView.vue";
import CompanySettingsView from "@/views/company/SettingsView.vue";
import CompanyPlacementsView from "@/views/company/PlacementsView.vue";
import CompanyDriveDetailsView from "@/views/company/DriveDetailsView.vue";
import StudentDashboardView from "@/views/student/DashboardView.vue";
import StudentJobsView from "@/views/student/JobsView.vue";
import StudentDriveDetailsView from "@/views/student/DriveDetailsView.vue";
import StudentApplicationsView from "@/views/student/ApplicationsView.vue";
import StudentInterviewsView from "@/views/student/InterviewsView.vue";
import StudentPlacementsView from "@/views/student/PlacementsView.vue";
import StudentProfileView from "@/views/student/ProfileView.vue";
import StudentSettingsView from "@/views/student/SettingsView.vue";

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
  // ADMIN ROUTES
  {
    path: "/admin",
    name: "admin-dashboard",
    component: AdminDashboardView,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/admin/companies",
    name: "admin-company-dashboard",
    component: AdminCompaniesView,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/admin/students",
    name: "admin-student-dashboard",
    component: AdminStudentsView,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/admin/drives",
    name: "admin-drives-dashboard",
    component: AdminDrivesView,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/admin/applications",
    name: "admin-application-dashboard",
    component: AdminApplicationsView,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/admin/analytics",
    name: "admin-analytics-dashboard",
    component: AdminAnalyticsView,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/admin/reports",
    name: "admin-reports-dashboard",
    component: AdminReportsView,
    meta: { requiresAuth: true, role: "admin" },
  },
  // COMPANY ROUTES
  {
    path: "/company",
    name: "company-dashboard",
    component: CompanyDashboardView,
    meta: { requiresAuth: true, role: "company" },
  },
  {
    path: "/company/drives",
    name: "company-drives",
    component: CompanyDrivesView,
    meta: { requiresAuth: true, role: "company" },
  },
  {
    path: "/company/drives/:id",
    name: "company-drive-details",
    component: CompanyDriveDetailsView,
    meta: { requiresAuth: true, role: "company" },
  },
  {
    path: "/company/applications",
    name: "company-applications",
    component: CompanyApplicationsView,
    meta: { requiresAuth: true, role: "company" },
  },
  {
    path: "/company/interviews",
    name: "company-interviews",
    component: CompanyInterviewsView,
    meta: { requiresAuth: true, role: "company" },
  },
  {
    path: "/company/placements",
    name: "company-placements",
    component: CompanyPlacementsView,
    meta: { requiresAuth: true, role: "company" },
  },
  {
    path: "/company/profile",
    name: "company-profile",
    component: CompanyProfileView,
    meta: { requiresAuth: true, role: "company" },
  },
  {
    path: "/company/settings",
    name: "company-settings",
    component: CompanySettingsView,
    meta: { requiresAuth: true, role: "company" },
  },
  // STUDENT ROUTES
  {
    path: "/student",
    name: "student-dashboard",
    component: StudentDashboardView,
    meta: { requiresAuth: true, role: "student" },
  },
  {
    path: "/student/drives",
    name: "student-drives",
    component: StudentJobsView,
    meta: { requiresAuth: true, role: "student" },
  },
  {
    path: "/student/drives/:id",
    name: "student-drive-details",
    component: StudentDriveDetailsView,
    meta: { requiresAuth: true, role: "student" },
  },
  {
    path: "/student/applications",
    name: "student-applications",
    component: StudentApplicationsView,
    meta: { requiresAuth: true, role: "student" },
  },
  {
    path: "/student/interviews",
    name: "student-interviews",
    component: StudentInterviewsView,
    meta: { requiresAuth: true, role: "student" },
  },
  {
    path: "/student/placements",
    name: "student-placements",
    component: StudentPlacementsView,
    meta: { requiresAuth: true, role: "student" },
  },
  {
    path: "/student/profile",
    name: "student-profile",
    component: StudentProfileView,
    meta: { requiresAuth: true, role: "student" },
  },
  {
    path: "/student/settings",
    name: "student-settings",
    component: StudentSettingsView,
    meta: { requiresAuth: true, role: "student" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("user");

  if (to.meta.requiresAuth && !token) {
    return next("/login");
  }

  if (to.meta.role && role !== to.meta.role) {
    return next(token ? "/login" : "/login");
  }

  if ((to.name === "login" || to.name === "register") && token && role) {
    return next(`/${role}`);
  }

  next();
});

export default router;
