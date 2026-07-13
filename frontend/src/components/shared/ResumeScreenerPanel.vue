<template>
  <div class="ats-panel card shadow-sm border-0">
    <div class="card-body p-4">
      <div
        class="d-flex flex-column flex-lg-row justify-content-between gap-3 mb-4"
      >
        <div>
          <span class="ats-kicker">ATS Resume Screener</span>
          <h5 class="fw-bold mb-1">{{ title }}</h5>
          <p class="text-muted mb-0">
            {{ subtitle }}
          </p>
        </div>
        <div class="score-badge" :class="scoreTone">
          <span>{{ score }}</span>
          <small>Match</small>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-12 col-xl-7">
          <div class="row g-3">
            <div class="col-12 col-md-6">
              <label class="form-label">Target role</label>
              <input
                v-model="targetRole"
                type="text"
                class="form-control"
                placeholder="Frontend Engineer"
              />
            </div>
            <div class="col-12 col-md-6">
              <label class="form-label">Required experience</label>
              <input
                v-model="experienceNeed"
                type="text"
                class="form-control"
                placeholder="0-2 years, internship, projects"
              />
            </div>
            <div class="col-12">
              <label class="form-label">Required skills</label>
              <input
                v-model="skillsInput"
                type="text"
                class="form-control"
                placeholder="Vue, JavaScript, SQL, APIs"
              />
            </div>
            <div class="col-12">
              <label class="form-label">Job description / criteria</label>
              <textarea
                v-model="jobDescription"
                class="form-control ats-textarea"
                placeholder="Paste the job description, selection criteria, or drive requirements."
              ></textarea>
            </div>
            <div class="col-12">
              <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
                <label class="form-label mb-0">Resume text</label>
                <label class="btn btn-outline-primary btn-sm mb-0">
                  <i class="ti ti-upload me-1"></i>Upload text resume
                  <input
                    class="d-none"
                    type="file"
                    accept=".txt,.md,.csv,.json"
                    @change="handleFile"
                  />
                </label>
              </div>
              <textarea
                v-model="resumeText"
                class="form-control ats-resume"
                placeholder="Paste resume content here. Text files are supported for quick screening."
              ></textarea>
              <small v-if="fileError" class="text-danger d-block mt-2">
                {{ fileError }}
              </small>
            </div>
          </div>
        </div>

        <div class="col-12 col-xl-5">
          <div class="insight-stack">
            <div class="insight-card">
              <div class="d-flex justify-content-between gap-3 mb-2">
                <span class="fw-semibold">Keyword coverage</span>
                <span class="text-muted"
                  >{{ matchedSkills.length }}/{{ requiredSkills.length }}</span
                >
              </div>
              <div class="progress ats-progress">
                <div
                  class="progress-bar"
                  :class="scoreBarClass"
                  :style="{ width: `${keywordCoverage}%` }"
                ></div>
              </div>
            </div>

            <div class="insight-card">
              <div class="fw-semibold mb-2">Matched skills</div>
              <div v-if="matchedSkills.length" class="chip-list">
                <span
                  v-for="skill in matchedSkills"
                  :key="skill"
                  class="chip chip-good"
                >
                  {{ skill }}
                </span>
              </div>
              <small v-else class="text-muted"
                >No required skills found yet.</small
              >
            </div>

            <div class="insight-card">
              <div class="fw-semibold mb-2">Missing skills</div>
              <div v-if="missingSkills.length" class="chip-list">
                <span v-for="skill in missingSkills" :key="skill" class="chip">
                  {{ skill }}
                </span>
              </div>
              <small v-else class="text-muted"
                >All required skills are covered.</small
              >
            </div>

            <div class="insight-card">
              <div class="fw-semibold mb-2">ATS signals</div>
              <ul class="signal-list mb-0">
                <li v-for="signal in signals" :key="signal.label">
                  <i
                    :class="[
                      'ti',
                      signal.icon,
                      signal.ok ? 'text-success' : 'text-warning',
                    ]"
                  ></i>
                  <span>{{ signal.label }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";

defineProps({
  title: {
    type: String,
    default: "Screen a resume against a role",
  },
  subtitle: {
    type: String,
    default:
      "Paste criteria and resume text to estimate ATS fit before applying or shortlisting.",
  },
});

const targetRole = ref("");
const experienceNeed = ref("");
const skillsInput = ref("");
const jobDescription = ref("");
const resumeText = ref("");
const fileError = ref("");

const normalize = (value = "") => String(value).toLowerCase();

const uniqueWords = (value) =>
  Array.from(
    new Set(
      normalize(value)
        .split(/[^a-z0-9+#.]+/i)
        .map((item) => item.trim())
        .filter((item) => item.length >= 2),
    ),
  );

const requiredSkills = computed(() => {
  const skills = skillsInput.value
    .split(/[,;\n]/)
    .map((skill) => skill.trim())
    .filter(Boolean);

  return Array.from(new Set(skills));
});

const resume = computed(() => normalize(resumeText.value));
const criteriaText = computed(() =>
  [targetRole.value, experienceNeed.value, jobDescription.value]
    .filter(Boolean)
    .join(" "),
);

const matchedSkills = computed(() =>
  requiredSkills.value.filter((skill) =>
    resume.value.includes(normalize(skill)),
  ),
);

const missingSkills = computed(() =>
  requiredSkills.value.filter(
    (skill) => !resume.value.includes(normalize(skill)),
  ),
);

const keywordCoverage = computed(() => {
  if (!requiredSkills.value.length) return resumeText.value.trim() ? 35 : 0;
  return Math.round(
    (matchedSkills.value.length / requiredSkills.value.length) * 100,
  );
});

const criteriaCoverage = computed(() => {
  const keywords = uniqueWords(criteriaText.value).filter(
    (word) =>
      !["and", "the", "for", "with", "from", "this", "that"].includes(word),
  );
  if (!keywords.length || !resumeText.value.trim()) return 0;
  const hits = keywords.filter((word) => resume.value.includes(word)).length;
  return Math.round((hits / keywords.length) * 100);
});

const hasContactSignal = computed(
  () =>
    /[^\s@]+@[^\s@]+\.[^\s@]+/.test(resumeText.value) ||
    /\b\d{10}\b/.test(resumeText.value),
);
const hasProjectSignal = computed(() =>
  /\b(project|portfolio|github|internship|experience|built|developed)\b/i.test(
    resumeText.value,
  ),
);
const hasEducationSignal = computed(() =>
  /\b(education|degree|b\.?tech|bachelor|cgpa|gpa|university|college)\b/i.test(
    resumeText.value,
  ),
);

const score = computed(() => {
  if (!resumeText.value.trim()) return 0;
  const structureScore =
    [
      hasContactSignal.value,
      hasProjectSignal.value,
      hasEducationSignal.value,
    ].filter(Boolean).length * 8;
  return Math.min(
    100,
    Math.round(
      keywordCoverage.value * 0.55 +
        criteriaCoverage.value * 0.25 +
        structureScore,
    ),
  );
});

const scoreTone = computed(() => {
  if (score.value >= 75) return "score-good";
  if (score.value >= 50) return "score-mid";
  return "score-low";
});

const scoreBarClass = computed(() => {
  if (keywordCoverage.value >= 75) return "bg-success";
  if (keywordCoverage.value >= 50) return "bg-warning";
  return "bg-danger";
});

const signals = computed(() => [
  {
    label: "Contact information detected",
    ok: hasContactSignal.value,
    icon: hasContactSignal.value ? "ti-circle-check" : "ti-alert-circle",
  },
  {
    label: "Projects or experience mentioned",
    ok: hasProjectSignal.value,
    icon: hasProjectSignal.value ? "ti-circle-check" : "ti-alert-circle",
  },
  {
    label: "Education details included",
    ok: hasEducationSignal.value,
    icon: hasEducationSignal.value ? "ti-circle-check" : "ti-alert-circle",
  },
]);

const handleFile = async (event) => {
  fileError.value = "";
  const [file] = event.target.files || [];
  if (!file) return;

  if (file.size > 1024 * 1024) {
    fileError.value = "Use a text file smaller than 1 MB.";
    event.target.value = "";
    return;
  }

  try {
    resumeText.value = await file.text();
  } catch (error) {
    fileError.value =
      "Could not read this file. Paste the resume text instead.";
  } finally {
    event.target.value = "";
  }
};
</script>

<style scoped>
.ats-panel {
  border-radius: 1rem;
}

.ats-kicker {
  display: inline-flex;
  color: #0d6efd;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 0.35rem;
}

.score-badge {
  width: 104px;
  height: 104px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  align-content: center;
  border: 1px solid #e5e7eb;
  background: #f8fafc;
  flex: 0 0 auto;
}

.score-badge span {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1;
}

.score-badge small {
  color: #6b7280;
}

.score-good {
  color: #047857;
  background: #ecfdf5;
  border-color: #bbf7d0;
}

.score-mid {
  color: #b45309;
  background: #fffbeb;
  border-color: #fde68a;
}

.score-low {
  color: #b91c1c;
  background: #fef2f2;
  border-color: #fecaca;
}

.ats-textarea {
  min-height: 110px;
}

.ats-resume {
  min-height: 220px;
}

.insight-stack {
  display: grid;
  gap: 1rem;
}

.insight-card {
  border: 1px solid #e9eef5;
  border-radius: 0.9rem;
  padding: 1rem;
  background: #fff;
}

.ats-progress {
  height: 0.65rem;
}

.chip-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.chip {
  border-radius: 999px;
  padding: 0.35rem 0.65rem;
  background: #f1f5f9;
  color: #475569;
  font-size: 0.82rem;
  font-weight: 600;
}

.chip-good {
  background: #ecfdf5;
  color: #047857;
}

.signal-list {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 0.75rem;
}

.signal-list li {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  color: #334155;
}
</style>
