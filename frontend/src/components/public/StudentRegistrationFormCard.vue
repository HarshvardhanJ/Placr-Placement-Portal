<template>
  <div
    class="company-register-panel d-flex flex-column flex-grow-1 align-items-center justify-content-center bg-white w-100 py-1 px-3 px-lg-0"
  >
    <div class="card shadow-sm w-100 mt-6" style="max-width: 480px">
      <div class="card-body p-3 my-3">
        <h2 class="fw-bold text-center mb-2">Create Student Account</h2>
        <p class="text-center text-secondary mb-4">
          Join to unlock the portal to countless opportunities.
        </p>

        <form class="needs-validation" novalidate @submit.prevent="studentSignup">
          <div class="mb-3">
            <label class="form-label">Full Name</label>

            <div class="input-icon">
              <span class="input-icon-addon">
                <img :src="userIcon" alt="User" width="18" height="18" />
              </span>

              <input
                v-model="name"
                type="text"
                class="form-control"
                :class="{ 'is-invalid': submitted && nameError }"
                placeholder="Your Name"
                autocomplete="name"
                required
              />
              <div class="invalid-feedback">{{ nameError }}</div>
            </div>
          </div>
          <div class="mb-2">
            <label class="form-label">Institutional Email</label>
            <div class="input-icon">
              <span class="input-icon-addon">
                <img :src="mailIcon" alt="mail" width="18" height="18" />
              </span>
              <input
                v-model="email"
                type="email"
                class="form-control"
                :class="{ 'is-invalid': submitted && emailError }"
                placeholder="student@university.ac.in"
                autocomplete="email"
                required
              />
              <div class="invalid-feedback">{{ emailError }}</div>
            </div>
          </div>

          <div class="mb-2">
            <label class="form-label">Roll Number</label>
            <div class="input-icon">
              <span class="input-icon-addon">
                <img :src="schoolIcon" alt="rolNo" width="18" height="18" />
              </span>
              <input
                v-model="roll_no"
                type="text"
                class="form-control"
                :class="{ 'is-invalid': submitted && rollNoError }"
                placeholder="24CS123"
                required
              />
              <div class="invalid-feedback">{{ rollNoError }}</div>
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
                    alt="passwordCheck"
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
            {{ submitting ? "Creating..." : "Create Account" }}
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
import userIcon from "@/assets/icons/user.svg";
import lockIcon from "@/assets/icons/lock.svg";
import lockCheckIcon from "@/assets/icons/lock-check.svg";
import mailIcon from "@/assets/icons/mail.svg";
import schoolIcon from "@/assets/icons/school.svg";

const router = useRouter();
const authStore = useAuthStore();

const name = ref("");
const email = ref("");
const roll_no = ref("");
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

const nameError = computed(() =>
  name.value.trim().length >= 2 ? "" : "Full name must be at least 2 characters.",
);
const emailError = computed(() => {
  if (!email.value.trim()) return "Institutional email is required.";
  if (!emailPattern.test(email.value.trim())) return "Enter a valid email address.";
  return "";
});
const rollNoError = computed(() =>
  roll_no.value.trim() ? "" : "Roll number is required.",
);
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
    !nameError.value &&
    !emailError.value &&
    !rollNoError.value &&
    !passwordError.value &&
    !confirmPasswordError.value,
);

async function studentSignup() {
  submitted.value = true;
  error.value = "";

  try {
    if (!formValid.value) return;
    submitting.value = true;
    await api.post("/auth/register/student", {
      name: name.value.trim(),
      email: email.value.trim().toLowerCase(),
      roll_no: roll_no.value.trim(),
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
