<template>
  <div
    class="company-register-panel d-flex flex-column flex-grow-1 align-items-center justify-content-center bg-white w-100 py-1 px-3 px-lg-0"
  >
    <div class="card shadow-sm w-100 mt-6" style="max-width: 480px">
      <div class="card-body p-3 my-3">
        <h2 class="fw-bold text-center mb-2">Register Your Company</h2>
        <p class="text-center text-secondary mb-4">
          Join the premier placement portal to find top talent.
        </p>

        <div
          class="alert info-alert d-flex align-items-start gap-3 mb-4"
          role="alert"
        >
          <img
            :src="infoIcon"
            alt="Info"
            width="20"
            height="20"
            class="mt-1 flex-shrink-0"
          />

          <div>
            Company accounts require approval by the placement administrator.
          </div>
        </div>
        <form @submit.prevent="companySignup">
          <div class="mb-2">
            <label class="form-label">Company Name</label>
            <input
              v-model="compnayName"
              type="text"
              class="form-control"
              placeholder="Some Corp"
            />
          </div>
          <div class="mb-2">
            <label class="form-label">Company Email</label>
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="hr@company.com"
            />
          </div>

          <div class="row mb-2">
            <div class="col-md-6 mb-3">
              <label class="form-label">Password</label>
              <input
                v-model="password"
                type="password"
                class="form-control"
                placeholder="••••••••"
              />
            </div>

            <div class="col-md-6 mb-3">
              <label class="form-label">Confirm Password</label>
              <input
                v-model="confirmPassword"
                type="password"
                class="form-control"
                placeholder="••••••••"
              />
            </div>
          </div>

          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>

          <button type="submit" class="btn btn-primary w-100">
            Register Company
          </button>
        </form>
      </div>
    </div>
    <div class="my-3">
      <RouterLink to="/login" class="btn btn-link"> Sign In </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "@/services/api";
import { useAuthStore } from "@/stores/authStore";
import { useRouter } from "vue-router";
import infoIcon from "@/assets/info-circle.svg";

const router = useRouter();
const authStore = useAuthStore();

const companyName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const error = ref("");

async function companySignup() {
  error.value = "";

  try {
    if (password.value !== confirmPassword.value) {
      error.value = "Passwords do not match";
      return;
    }
    const response = await api.post("/auth/register/company", {
      name: companyName.value,
      email: email.value,
      password: password.value,
      repeat_password: confirmPassword.value,
    });
    router.push("/login");
  } catch (err) {
    error.value =
      err?.response?.data?.error || `Sign up failed. Please try again. ${err}`;
  }
}
</script>

<style scoped>
.company-register-panel {
  min-height: 100%;
}

.info-alert {
  border-left: 4px solid var(--bs-primary);
  border-radius: 0.5rem;
  background-color: rgba(var(--bs-primary-rgb), 0.08);
}
</style>
