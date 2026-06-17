import { createRouter, createWebHistory } from "vue-router";

import LoginView from "@/views/auth/LoginView.vue";
import StudentRegisterView from "@/views/auth/StudentRegisterView.vue";
import CompanyRegisterView from "@/views/auth/CompanyRegisterView.vue";
import LandingView from "@/views/auth/LandingView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";

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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
