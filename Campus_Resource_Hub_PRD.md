# Campus Resource Hub — Product Requirements Document (PRD)

**Course:** AiDD / X501 – AI-Driven Development  
**Instructor:** Prof. Jay Newquist  
**Team Repo:** [https://github.com/sofisch25/AiDD-Final-Project.git](https://github.com/sofisch25/AiDD-Final-Project.git)  
**Team Role:** Product Lead – PRD Owner  

---

## 1. Context & Problem
University departments and student groups lack a centralized system for discovering and reserving shared resources. Current manual methods (emails, spreadsheets, paper sign-ups) cause double bookings, underuse, and frustration.

**Problem Statement:**  
“Students and staff waste time coordinating resources manually because there is no unified, searchable system for reserving campus assets.”

---

## 2. Goals
1. Centralize campus resources (rooms, equipment, spaces) into a searchable catalog.  
2. Enable easy booking with automated conflict detection.  
3. Provide transparent workflows for approvals and reviews.  
4. Deliver an accessible, user-friendly web experience.  
5. Integrate an AI-assisted feature (Resource Concierge or AI Scheduler).  

---

## 3. Non-Goals
- No payment or billing.  
- No native mobile app (responsive web only).  
- No external SSO beyond email/password.  
- No real-time chat.  

---

## 4. Users & Key Flows

| User Type | Primary Goal | Typical Flow |
|------------|---------------|---------------|
| **Student** | Reserve rooms/equipment. | Search → View → Request → Confirm. |
| **Staff/Faculty** | Manage and approve departmental resources. | Add/Edit → Review → Approve/Reject. |
| **Admin** | Oversee users and moderate content. | Admin Dashboard → Reports → Moderation. |

**Example User Story:**  
“As a student, I want to view available study rooms for a specific date so I can plan my group project meetings.”

---

## 5. MVP vs. Nice-to-Have

| Category | Must-Have (MVP) | Nice-to-Have | Future Iteration |
|-----------|----------------|---------------|------------------|
| Auth | Register/Login/Logout | OAuth | MFA |
| Listings | CRUD Resources | Image uploads | Bulk import |
| Search | Keyword + Date Filter | Advanced Search | AI-semantic search |
| Booking | Conflict detection | Calendar sync | Waitlists |
| Messaging | Threaded text | File attachments | Real-time chat |
| AI Feature | Resource Concierge | AI Scheduler | Predictive analytics |

---

## 6. Hypothesis & Assumptions

*If users can search and book resources through a centralized app, booking conflicts and coordination time will drop by at least 40% within the first semester.*

| Dimension | Key Assumption | Validation Plan |
|------------|----------------|-----------------|
| **Desirability** | Users prefer one-stop booking. | UX tests, early feedback. |
| **Feasibility** | Flask + SQLite scales to pilot. | Technical prototype. |
| **Viability** | Admins save time via automation. | Compare pre/post booking logs. |

---

## 7. Success Metrics

| Metric | Target |
|---------|---------|
| Conflict-free bookings | 100% in testing |
| Booking flow completion | ≥ 90% of test users |
| Avg. booking time | ↓ ≥ 40% from baseline |
| User satisfaction | ≥ 4 / 5 |
| AI feature accuracy | ≥ 80% relevant answers |

---

## 8. Risks & Mitigation

| Risk | Likelihood | Mitigation |
|------|-------------|-------------|
| Scope creep | Medium | Freeze MVP after Day 6. |
| AI hallucination | Medium | Limit to verified DB data. |
| Low adoption | Medium | Validate wireframes early. |
| Technical delays | High | Use 18-day sprint plan. |

---

## 9. Delivery Plan (18-Day Schedule)

| Phase | Focus | Deliverables |
|--------|--------|--------------|
| Days 1-3 | Planning & Setup | PRD, Wireframes, Repo |
| Days 4-6 | Database + Auth | Schema, login flow |
| Days 7-9 | CRUD + Search | Listings, filters |
| Days 10-12 | Booking + Messaging | Conflict logic, threads |
| Days 13-14 | UI Polish | Accessibility, testing UX |
| Day 15 | Testing & Security | pytest results |
| Days 16-18 | Docs + Demo | README, ERD, Slides |
