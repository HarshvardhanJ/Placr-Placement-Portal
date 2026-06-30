<template>
  <div
    class="login-panel d-flex flex-column align-items-center justify-content-center bg-white h-100 px-3 px-lg-0"
  >
    <div class="mb-4">
      <img :src="placrLogo" alt="PLACR" class="login-logo rounded-3" />
    </div>

    <div class="login-card card shadow-sm w-100">
      <div class="card-body">
        <h2 class="fw-bold text-center mb-2">Sign In</h2>
        <p class="text-center text-secondary mb-4">Access your dashboard</p>

        <form @submit.prevent="login">
          <div class="mb-3">
            <label class="form-label">Email Address</label>
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="you@example.com"
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

          <div class="d-flex justify-content-between align-items-center mb-4">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" id="rememberMe" />
              <label class="form-check-label" for="rememberMe">
                Remember me
              </label>
            </div>

            <a href="#" class="text-decoration-none">Forgot password?</a>
          </div>

          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>

          <button type="submit" class="btn btn-primary w-100">Sign In</button>
        </form>

        <div class="text-center mt-4">
          Don't have an account?
          <RouterLink to="/register">Create Account</RouterLink>
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
import placrLogo from "@/assets/placr.png";

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

<style scoped>
.login-panel {
  min-height: 100%;
  padding-block: clamp(2.5rem, 5vh, 4rem);
}

.login-logo {
  width: 90px;
  height: 90px;
  object-fit: contain;
}

.login-card {
  max-width: 480px;
  border-radius: 0.65rem;
}

.login-card .card-body {
  min-height: 430px;
  padding: 2rem;
}

.login-card h2 {
  font-size: 1.75rem;
}

.form-control {
  min-height: 44px;
}

.btn[type="submit"] {
  min-height: 44px;
}

@media (max-width: 575.98px) {
  .login-card .card-body {
    min-height: auto;
    padding: 1.5rem;
  }
}

@media (max-width: 991.98px) {
  .login-panel {
    min-height: calc(100vh - 100px);
  }
}
</style>
