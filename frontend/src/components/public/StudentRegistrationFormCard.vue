<template>
  <div
    class="d-flex align-items-center justify-content-center bg-white h-100 py-5 px-3 px-lg-0"
  >
    <div class="card shadow-sm border-0 w-100" style="max-width: 480px">
      <div class="card-body p-5">
        <h2 class="fw-bold text-center mb-2">Sign In</h2>
        <p class="text-center text-secondary mb-4">Access your dashboard</p>

        <form @submit.prevent="companySignup">
          <div class="mb-3">
            <label class="form-label">Company Name</label>
            <input
              v-model="compnayName"
              type="text"
              class="form-control"
              placeholder="Some Corp"
            />
          </div>
          <div class="mb-3">
            <label class="form-label">HR Name</label>
            <input
              v-model="hrName"
              type="text"
              class="form-control"
              placeholder="First Last"
            />
          </div>
          <div class="mb-3">
            <label class="form-label">Company Email</label>
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="hr@company.com"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input
              v-model="password"
              type="password"
              class="form-control"
              placeholder="••••••••"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Confirm Password</label>
            <input
              v-model="repeatPassword"
              type="password"
              class="form-control"
              placeholder="••••••••"
            />
          </div>

          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>

          <button type="submit" class="btn btn-primary w-100">Sign In</button>
        </form>

        <div class="text-center mt-4">
          Don't have an account?
          <RouterLink to="/register/student">Create Account</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "@/services/api";
import { useAuthStore } from "@/stores/authStore";
import { useRouter } from "vue-router";

const router = useRouter();
const authStore = useAuthStore();

const email = ref("");
const password = ref("");
const error = ref("");

async function login() {
  error.value = "";

  try {
    const response = await api.post("/auth/login", {
      email: email.value,
      password: password.value,
    });

    const role = response.data.user.role;

    authStore.login(response.data.token, role);

    if (role === "admin") {
      router.push("/admin");
    } else if (role === "company") {
      router.push("/company");
    } else {
      router.push("/student");
    }
  } catch (err) {
    error.value =
      err?.response?.data?.error || "Login failed. Please try again.";
  }
}
</script>
