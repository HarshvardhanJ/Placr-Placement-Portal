<template>
  <CompanyLayout :show-search="false">
    <PageHeader
      title="Settings"
      subtitle="Manage your account security and preferences."
    />

    <div class="row g-4">
      <div class="col-12 col-lg-7">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white">
            <h5 class="mb-0 fw-semibold">Change Password</h5>
          </div>
          <div class="card-body">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <div v-if="success" class="alert alert-success">{{ success }}</div>

            <form @submit.prevent="changePassword">
              <div class="mb-3">
                <label class="form-label">Current Password</label>
                <input
                  v-model="form.current_password"
                  type="password"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">New Password</label>
                <input
                  v-model="form.new_password"
                  type="password"
                  class="form-control"
                  required
                />
                <small class="text-muted">
                  At least 8 characters, with uppercase, lowercase, and a
                  number.
                </small>
              </div>

              <div class="mb-3">
                <label class="form-label">Repeat New Password</label>
                <input
                  v-model="form.repeat_password"
                  type="password"
                  class="form-control"
                  required
                />
              </div>

              <button type="submit" class="btn btn-primary" :disabled="saving">
                {{ saving ? "Updating..." : "Update Password" }}
              </button>
            </form>
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-5">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white">
            <h5 class="mb-0 fw-semibold">Notification Preferences</h5>
          </div>
          <div class="card-body">
            <p class="text-muted small">NOT COMPLETED YET / TODO</p>

            <div class="form-check form-switch mb-2">
              <input class="form-check-input" type="checkbox" disabled />
              <label class="form-check-label text-muted"
                >New applicant alerts</label
              >
            </div>
            <div class="form-check form-switch mb-2">
              <input class="form-check-input" type="checkbox" disabled />
              <label class="form-check-label text-muted"
                >Drive deadline reminders</label
              >
            </div>
            <div class="form-check form-switch">
              <input class="form-check-input" type="checkbox" disabled />
              <label class="form-check-label text-muted"
                >Monthly placement report email</label
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </CompanyLayout>
</template>

<script setup>
import { reactive, ref } from "vue";
import api from "@/services/api";

import CompanyLayout from "@/layouts/CompanyLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";

const saving = ref(false);
const error = ref("");
const success = ref("");

const form = reactive({
  current_password: "",
  new_password: "",
  repeat_password: "",
});

const resetForm = () => {
  form.current_password = "";
  form.new_password = "";
  form.repeat_password = "";
};

const changePassword = async () => {
  error.value = "";
  success.value = "";

  if (form.new_password !== form.repeat_password) {
    error.value = "New passwords do not match";
    return;
  }

  saving.value = true;
  try {
    await api.put("/auth/change-password", { ...form });
    success.value = "Password updated successfully";
    resetForm();
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to update password";
  } finally {
    saving.value = false;
  }
};
</script>
