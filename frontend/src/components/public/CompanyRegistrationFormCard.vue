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
        <form class="needs-validation" novalidate @submit.prevent="companySignup">
          <div class="mb-2">
            <label class="form-label">Company Name</label>
            <div class="input-icon">
              <span class="input-icon-addon">
                <img
                  :src="companyIcon"
                  alt="companyName"
                  width="18"
                  height="18"
                />
              </span>
              <input
                v-model="companyName"
                type="text"
                class="form-control"
                :class="{ 'is-invalid': submitted && companyNameError }"
                placeholder="Some Corp"
                autocomplete="organization"
                required
              />
              <div class="invalid-feedback">{{ companyNameError }}</div>
            </div>
          </div>
          <div class="mb-2">
            <label class="form-label">Company Email</label>
            <div class="input-icon">
              <span class="input-icon-addon">
                <img :src="mailIcon" alt="email" width="18" height="18" />
              </span>

              <input
                v-model="email"
                type="email"
                class="form-control"
                :class="{ 'is-invalid': submitted && emailError }"
                placeholder="hr@company.com"
                autocomplete="email"
                required
              />
              <div class="invalid-feedback">{{ emailError }}</div>
            </div>
          </div>

          <div class="row mb-2">
            <div class="col-md-6 mb-3">
              <label class="form-label">Password</label>
              <div class="input-icon">
                <span class="input-icon-addon">
                  <img :src="lockIcon" alt="password" width="18" height="18" />
                </span>
                <input
                  v-model="password"
                  type="password"
                  class="form-control"
                  :class="{ 'is-invalid': submitted && passwordError }"
                  placeholder="••••••••"
                  autocomplete="new-password"
                  required
                />
                <div class="invalid-feedback">{{ passwordError }}</div>
              </div>
              <div class="mt-2 small">
                <div :class="hasMinLength ? 'text-success' : 'text-secondary'">
                  ✓ At least 8 characters
                </div>

                <div :class="hasUpperCase ? 'text-success' : 'text-secondary'">
                  ✓ One uppercase letter
                </div>

                <div :class="hasLowerCase ? 'text-success' : 'text-secondary'">
                  ✓ One lowercase letter
                </div>

                <div :class="hasNumber ? 'text-success' : 'text-secondary'">
                  ✓ One number
                </div>
              </div>
            </div>

            <div class="col-md-6 mb-3">
              <label class="form-label">Confirm Password</label>
              <div class="input-icon">
                <span class="input-icon-addon">
                  <img
                    :src="lockCheckIcon"
                    alt="password"
                    width="18"
                    height="18"
                  />
                </span>
                <input
                  v-model="confirmPassword"
                  type="password"
                  class="form-control"
                  :class="{ 'is-invalid': submitted && confirmPasswordError }"
                  placeholder="••••••••"
                  autocomplete="new-password"
                  required
                />
                <div class="invalid-feedback">{{ confirmPasswordError }}</div>
              </div>
              <div
                v-if="confirmPassword"
                class="small mt-2"
                :class="passwordsMatch ? 'text-success' : 'text-danger'"
              >
                {{
                  passwordsMatch ? "Passwords match" : "Passwords do not match"
                }}
              </div>
            </div>
          </div>

          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>

          <button
            type="submit"
            class="btn btn-primary w-100"
            :disabled="submitting"
          >
            {{ submitting ? "Registering..." : "Register Company" }}
          </button>
        </form>
      </div>
    </div>
    <div class="my-3">
      <span
        class="text-secondary text-decoration-none d-inline-flex align-items-center gap-1 hover-primary transition-colors"
        >Already have an account?
        <RouterLink to="/login" class="btn btn-link"> Sign In </RouterLink>
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import api from "@/services/api";
import { useAuthStore } from "@/stores/authStore";
import { useRouter } from "vue-router";
import infoIcon from "@/assets/icons/info-circle.svg";
import lockIcon from "@/assets/icons/lock.svg";
import lockCheckIcon from "@/assets/icons/lock-check.svg";
import mailIcon from "@/assets/icons/mail.svg";
import companyIcon from "@/assets/icons/building.svg";

const router = useRouter();
const authStore = useAuthStore();

const companyName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const error = ref("");
const submitted = ref(false);
const submitting = ref(false);
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const hasMinLength = computed(() => password.value.length >= 8);
const hasUpperCase = computed(() => /[A-Z]/.test(password.value));
const hasLowerCase = computed(() => /[a-z]/.test(password.value));
const hasNumber = computed(() => /\d/.test(password.value));

const passwordsMatch = computed(
  () =>
    confirmPassword.value.length > 0 &&
    password.value === confirmPassword.value,
);

const passwordValid = computed(
  () =>
    hasMinLength.value &&
    hasUpperCase.value &&
    hasLowerCase.value &&
    hasNumber.value,
);

const companyNameError = computed(() =>
  companyName.value.trim().length >= 2
    ? ""
    : "Company name must be at least 2 characters.",
);
const emailError = computed(() => {
  if (!email.value.trim()) return "Company email is required.";
  if (!emailPattern.test(email.value.trim())) return "Enter a valid email address.";
  return "";
});
const passwordError = computed(() =>
  passwordValid.value
    ? ""
    : "Password must meet all listed requirements.",
);
const confirmPasswordError = computed(() =>
  passwordsMatch.value ? "" : "Passwords must match.",
);
const formValid = computed(
  () =>
    !companyNameError.value &&
    !emailError.value &&
    !passwordError.value &&
    !confirmPasswordError.value,
);

async function companySignup() {
  submitted.value = true;
  error.value = "";

  try {
    if (!formValid.value) return;
    submitting.value = true;
    await api.post("/auth/register/company", {
      name: companyName.value.trim(),
      email: email.value.trim().toLowerCase(),
      password: password.value,
      repeat_password: confirmPassword.value,
    });
    router.push("/login");
  } catch (err) {
    error.value =
      err?.response?.data?.error || `Sign up failed. Please try again.`;
  } finally {
    submitting.value = false;
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
