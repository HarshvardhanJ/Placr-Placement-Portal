<template>
  <CompanyLayout>
    <PageHeader
      title="Company Profile"
      subtitle="Keep your company details up to date for students and admin."
    />

    <div v-if="loading" class="card shadow-sm p-5 text-center">
      Loading profile...
    </div>

    <div v-else class="row g-4">
      <div class="col-12 col-lg-8">
        <div class="card shadow-sm border-0">
          <div class="card-body">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <div v-if="success" class="alert alert-success">{{ success }}</div>

            <form @submit.prevent="save">
              <fieldset :disabled="profile.approval_status !== 'approved'">
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label">Company Name</label>
                    <input
                      :value="profile.name"
                      type="text"
                      class="form-control"
                      readonly
                    />
                    <small class="text-muted"
                      >Contact admin to change your registered name.</small
                    >
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Account Email</label>
                    <input
                      :value="email"
                      type="text"
                      class="form-control"
                      readonly
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Industry</label>
                    <input
                      v-model="form.industry"
                      type="text"
                      class="form-control"
                      placeholder="e.g. Software, Manufacturing"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Location</label>
                    <input
                      v-model="form.location"
                      type="text"
                      class="form-control"
                      placeholder="e.g. Bengaluru, India"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Website</label>
                    <input
                      v-model="form.website"
                      type="text"
                      class="form-control"
                      placeholder="https://example.com"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Contact</label>
                    <input
                      v-model="form.contact"
                      type="text"
                      class="form-control"
                      placeholder="HR contact email or phone"
                    />
                  </div>

                  <div class="col-12">
                    <label class="form-label">About the Company</label>
                    <textarea
                      v-model="form.description"
                      class="form-control"
                      rows="4"
                      placeholder="A short description students will see"
                    ></textarea>
                  </div>
                </div>

                <p
                  v-if="profile.approval_status !== 'approved'"
                  class="text-muted small mt-3 mb-0"
                >
                  Profile editing unlocks once admin approves your company.
                </p>
              </fieldset>

              <div class="mt-4 d-flex justify-content-end">
                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="saving || profile.approval_status !== 'approved'"
                >
                  {{ saving ? "Saving..." : "Save Changes" }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-4">
        <div class="card shadow-sm border-0">
          <div class="card-body">
            <h6 class="text-secondary mb-3">Account Status</h6>
            <span class="badge rounded-pill" :class="statusBadgeClass">
              {{ formatStatus(profile.approval_status) }}
            </span>
            <p class="text-muted mt-3 mb-0 small">
              {{
                profile.approval_status === "approved"
                  ? "Your company is approved and can post placement drives."
                  : "Your company is awaiting admin approval. You won't be able to post drives until approved."
              }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </CompanyLayout>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import api from "@/services/api";

import CompanyLayout from "@/layouts/CompanyLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";

const loading = ref(false);
const saving = ref(false);
const error = ref("");
const success = ref("");
const email = ref("");

const profile = reactive({
  name: "",
  approval_status: "",
});

const form = reactive({
  industry: "",
  location: "",
  website: "",
  contact: "",
  description: "",
});

const statusBadgeClass = computed(() =>
  profile.approval_status === "approved"
    ? "text-bg-success"
    : "text-bg-warning",
);

const formatStatus = (status = "") =>
  status === "approved" ? "Approved" : "Pending Approval";

const loadProfile = async () => {
  loading.value = true;
  error.value = "";
  try {
    const [{ data: profileData }, { data: meData }] = await Promise.all([
      api.get("/company/profile"),
      api.get("/auth/me"),
    ]);

    profile.name = profileData.name;
    profile.approval_status = profileData.approval_status;
    email.value = meData.email;

    form.industry = profileData.industry || "";
    form.location = profileData.location || "";
    form.website = profileData.website || "";
    form.contact = profileData.contact || "";
    form.description = profileData.description || "";
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to load profile";
  } finally {
    loading.value = false;
  }
};

const save = async () => {
  saving.value = true;
  error.value = "";
  success.value = "";
  try {
    await api.put("/company/profile", { ...form });
    success.value = "Profile updated successfully";
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to update profile";
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadProfile();
});
</script>
