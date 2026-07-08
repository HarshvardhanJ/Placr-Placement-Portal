<template>
  <StudentLayout :show-search="false">
    <PageHeader
      title="Profile"
      subtitle="Update education, skills, resume, and experience."
    >
      <template #actions>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink to="/student/drives" class="btn btn-outline-primary">
            <i class="ti ti-briefcase me-2"></i>Drives
          </RouterLink>
          <RouterLink to="/student/settings" class="btn btn-primary">
            <i class="ti ti-settings me-2"></i>Settings
          </RouterLink>
        </div>
      </template>
    </PageHeader>

    <div
      v-if="store.profileWarning"
      class="alert alert-warning d-flex align-items-center gap-2"
    >
      <i class="ti ti-alert-triangle"></i>
      <span
        >Complete your profile to unlock eligible drives and better application
        matching.</span
      >
    </div>

    <div v-if="store.error" class="alert alert-danger">
      {{ store.error }}
    </div>

    <div class="profile-shell">
      <div class="profile-hero card shadow-sm border-0 mb-4">
        <div
          class="card-body p-4 p-lg-5 d-flex flex-column flex-lg-row gap-4 align-items-lg-center justify-content-between"
        >
          <div class="d-flex align-items-center gap-3">
            <div class="profile-avatar">
              {{ initials }}
            </div>
            <div>
              <span class="hero-kicker">Student Profile</span>
              <h3 class="fw-bold mb-1">{{ profileName }}</h3>
              <p class="text-muted mb-0">
                Keep your profile current so eligibility and application data
                stay accurate.
              </p>
            </div>
          </div>

          <div class="d-flex flex-wrap gap-2">
            <RouterLink
              to="/student/applications"
              class="btn btn-outline-primary"
            >
              <i class="ti ti-file-text me-2"></i>Applications
            </RouterLink>
            <RouterLink to="/student/placements" class="btn btn-primary">
              <i class="ti ti-trophy me-2"></i>Placements
            </RouterLink>
          </div>
        </div>
      </div>

      <div class="row g-4 align-items-start">
        <div class="col-12 col-xl-8">
          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <div
                class="d-flex align-items-start justify-content-between mb-4"
              >
                <div>
                  <h6 class="fw-semibold mb-1">Edit profile</h6>
                  <small class="text-muted"
                    >Update the details that companies use for
                    shortlisting</small
                  >
                </div>
                <span class="pill-label">{{
                  profileComplete ? "Complete" : "Incomplete"
                }}</span>
              </div>

              <form class="row g-3" @submit.prevent="saveProfile">
                <div class="col-12 col-md-6">
                  <label class="form-label">Full name</label>
                  <input
                    v-model="form.name"
                    type="text"
                    class="form-control"
                    placeholder="Your full name"
                  />
                </div>

                <div class="col-12 col-md-6">
                  <label class="form-label">Phone number</label>
                  <input
                    v-model="form.phone_number"
                    type="text"
                    class="form-control"
                    placeholder="Contact number"
                  />
                </div>

                <div class="col-12 col-md-6">
                  <label class="form-label">Department</label>
                  <input
                    v-model="form.department"
                    type="text"
                    class="form-control"
                    placeholder="Branch / department"
                  />
                </div>

                <div class="col-12 col-md-3">
                  <label class="form-label">CGPA</label>
                  <input
                    v-model="form.cgpa"
                    type="number"
                    step="0.01"
                    min="0"
                    max="10"
                    class="form-control"
                    placeholder="0.00"
                  />
                </div>

                <div class="col-12 col-md-3">
                  <label class="form-label">Year</label>
                  <select v-model="form.year" class="form-select">
                    <option value="">Select year</option>
                    <option value="1">1st Year</option>
                    <option value="2">2nd Year</option>
                    <option value="3">3rd Year</option>
                    <option value="4">4th Year</option>
                  </select>
                </div>

                <div class="col-12">
                  <label class="form-label">Skills</label>
                  <textarea
                    v-model="form.skills"
                    class="form-control"
                    rows="3"
                    placeholder="Comma-separated skills, e.g. Python, SQL, Communication"
                  ></textarea>
                </div>

                <div class="col-12">
                  <label class="form-label">Experience</label>
                  <textarea
                    v-model="form.experience"
                    class="form-control"
                    rows="5"
                    placeholder="Internships, projects, achievements, and relevant experience"
                  ></textarea>
                </div>

                <div class="col-12 d-flex flex-wrap gap-2 pt-2">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="saving"
                  >
                    <span
                      v-if="saving"
                      class="spinner-border spinner-border-sm me-2"
                    ></span>
                    Save Profile
                  </button>
                  <button
                    type="button"
                    class="btn btn-outline-secondary"
                    @click="resetForm"
                  >
                    Reset
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <div class="col-12 col-xl-4 d-flex flex-column gap-4">
          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <div
                class="d-flex align-items-start justify-content-between mb-3"
              >
                <div>
                  <h6 class="fw-semibold mb-1">Resume</h6>
                  <small class="text-muted"
                    >Upload your latest resume in PDF format</small
                  >
                </div>
                <i class="ti ti-file-upload text-primary"></i>
              </div>

              <div class="resume-box">
                <div class="resume-status" :class="{ ok: hasResume }">
                  <i
                    :class="hasResume ? 'ti ti-file-check' : 'ti ti-file-off'"
                  ></i>
                  <span>{{
                    hasResume ? "Resume uploaded" : "No resume uploaded"
                  }}</span>
                </div>

                <p class="text-muted small mb-3">
                  {{
                    hasResume
                      ? `Current file: ${profileData.resume_filename || "resume.pdf"}. You can replace it anytime.`
                      : "Upload a PDF so you can apply to drives."
                  }}
                </p>

                <input
                  ref="resumeInput"
                  type="file"
                  accept=".pdf"
                  class="d-none"
                  @change="handleResumeUpload"
                />

                <div class="d-flex flex-wrap gap-2">
                  <button
                    type="button"
                    class="btn btn-outline-primary btn-sm"
                    @click="triggerResumePicker"
                  >
                    {{ hasResume ? "Replace Resume" : "Upload Resume" }}
                  </button>
                  <button
                    v-if="hasResume"
                    type="button"
                    class="btn btn-outline-secondary btn-sm"
                    @click="viewResume"
                  >
                    View Resume
                  </button>
                  <span v-if="hasResume" class="text-muted small align-self-center">
                    {{ profileData.resume_filename || "Resume uploaded" }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <div
                class="d-flex align-items-start justify-content-between mb-3"
              >
                <div>
                  <h6 class="fw-semibold mb-1">Profile summary</h6>
                  <small class="text-muted"
                    >Quick snapshot of your current data</small
                  >
                </div>
                <i class="ti ti-id-badge-2 text-primary"></i>
              </div>

              <div class="summary-stack">
                <div class="summary-item">
                  <div class="summary-label">Department</div>
                  <div class="summary-value">
                    {{ profileData.department || "Not set" }}
                  </div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">CGPA</div>
                  <div class="summary-value">
                    {{ profileData.cgpa ?? "Not set" }}
                  </div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">Year</div>
                  <div class="summary-value">
                    {{
                      profileData.year ? `${profileData.year} Year` : "Not set"
                    }}
                  </div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">Phone</div>
                  <div class="summary-value">
                    {{ profileData.phone_number || "Not set" }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <h6 class="fw-semibold mb-2">Need help completing this?</h6>
              <p class="text-muted small mb-3">
                Add your academics, skills, and resume first. That unlocks the
                most accurate drive recommendations.
              </p>
              <div class="d-flex flex-wrap gap-2">
                <RouterLink
                  to="/student/drives"
                  class="btn btn-outline-primary btn-sm"
                >
                  Browse Drives
                </RouterLink>
                <RouterLink
                  to="/student/applications"
                  class="btn btn-outline-secondary btn-sm"
                >
                  Applications
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </StudentLayout>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue";
import { storeToRefs } from "pinia";
import StudentLayout from "@/layouts/StudentLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import { useStudentStore } from "@/stores/studentStore";

const store = useStudentStore();
const { profile } = storeToRefs(store);

const saving = ref(false);
const resumeInput = ref(null);

const form = reactive({
  name: "",
  department: "",
  cgpa: "",
  year: "",
  phone_number: "",
  skills: "",
  experience: "",
});

const profileData = computed(() => profile.value ?? {});
const profileName = computed(() => profile.value?.name || "Student");
const initials = computed(() => {
  const name = profileName.value;
  return (
    name
      .split(" ")
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase())
      .join("") || "ST"
  );
});

const profileComplete = computed(() =>
  Boolean(
    profile.value?.department && profile.value?.cgpa && profile.value?.year,
  ),
);

const hasResume = computed(() =>
  Boolean(
    profile.value?.resume_uploaded ||
    profile.value?.resume_path ||
    profile.value?.resume_url ||
    profile.value?.resume,
  ),
);


const loadForm = () => {
  form.name = profile.value?.name || "";
  form.department = profile.value?.department || "";
  form.cgpa = profile.value?.cgpa ?? "";
  form.year = profile.value?.year ?? "";
  form.phone_number = profile.value?.phone_number || "";
  form.skills = profile.value?.skills || "";
  form.experience = profile.value?.experience || "";
};

const resetForm = () => {
  loadForm();
};

const saveProfile = async () => {
  saving.value = true;
  try {
    const payload = {
      name: form.name?.trim() || null,
      department: form.department?.trim() || null,
      cgpa: form.cgpa === "" || form.cgpa === null ? null : Number(form.cgpa),
      year: form.year === "" || form.year === null ? null : Number(form.year),
      phone_number: form.phone_number?.trim() || null,
      skills: form.skills?.trim() || null,
      experience: form.experience?.trim() || null,
    };

    await store.updateProfile(payload);
  } finally {
    saving.value = false;
  }
};

const triggerResumePicker = () => {
  resumeInput.value?.click();
};

const handleResumeUpload = async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;

  if (!file.name.toLowerCase().endsWith(".pdf")) {
    store.error = "Only PDF files are allowed";
    event.target.value = "";
    return;
  }

  try {
    await store.uploadResume(file);
  } finally {
    event.target.value = "";
  }
};

const viewResume = async () => {
  try {
    const response = await store.downloadResume();
    const blobUrl = URL.createObjectURL(response.data);
    window.open(blobUrl, "_blank", "noopener,noreferrer");
    setTimeout(() => URL.revokeObjectURL(blobUrl), 60_000);
  } catch (error) {
    store.error = error?.response?.data?.error || error?.message || "Failed to open resume";
  }
};

onMounted(async () => {
  await store.fetchProfile();
});

watch(
  profile,
  () => {
    loadForm();
  },
  { immediate: true },
);
</script>

<style scoped>
.profile-shell {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.profile-hero {
  border-radius: 1rem;
  background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
}

.hero-kicker {
  display: inline-flex;
  align-items: center;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #0d6efd;
  margin-bottom: 0.35rem;
}

.profile-avatar {
  width: 62px;
  height: 62px;
  border-radius: 18px;
  background: linear-gradient(135deg, #eef4ff, #dbeafe);
  color: #0d6efd;
  display: grid;
  place-items: center;
  font-weight: 800;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.pill-label {
  display: inline-flex;
  align-items: center;
  padding: 0.38rem 0.7rem;
  border-radius: 999px;
  background: #eef4ff;
  color: #0d6efd;
  font-size: 0.78rem;
  font-weight: 700;
}

.resume-box {
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 16px;
  background: #fff;
}

.resume-status {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.4rem 0.65rem;
  border-radius: 999px;
  background: #fff3cd;
  color: #8a6d3b;
  font-size: 0.82rem;
  font-weight: 700;
  margin-bottom: 0.9rem;
}

.resume-status.ok {
  background: #e8f8ef;
  color: #047857;
}

.summary-stack {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.summary-item {
  padding: 0.9rem;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  background: #fff;
}

.summary-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.summary-value {
  font-weight: 700;
  color: #111827;
}
</style>
