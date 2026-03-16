# 9장. Git 관련 에러: 코드 배포의 연결고리

## 학습 목표

Render.com은 GitHub 기반으로 배포한다. Git과 GitHub에서 발생하는 문제가 **배포 실패로 직결**되는 구조를 이해하고, 자주 만나는 Git 에러를 해결하는 방법을 배운다.

---

## 9.1 Git → GitHub → Render 배포 흐름

### 전체 흐름

```
내 컴퓨터                  GitHub                  Render
─────────                ────────                ────────
코드 수정
    ↓
git add .
    ↓
git commit
    ↓
git push ──────────→  저장소에 코드 반영 ──────→  자동 배포 시작
                                                   ↓
                                               빌드 + 서버 시작
                                                   ↓
                                               사이트에 반영
```

### 어디서 에러가 나는가?

| 단계 | 에러 확인 장소 | 상황 |
|------|-------------|------|
| `git add` / `git commit` | 내 터미널 | 커밋 자체가 안 됨 |
| `git push` | 내 터미널 | GitHub에 올리기 실패 |
| 자동 배포 | Render 대시보드 Deploy 로그 | 빌드/시작 실패 |
| 코드 누락 | Render Runtime 로그 | 필요한 파일이 안 올라감 |

---

## 9.2 자주 만나는 Git 에러들

### `git push` 거부 (rejected)

```
! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'github.com:myuser/myapp.git'
hint: Updates were rejected because the remote contains work that you do not have locally.
```

**원인:** GitHub에 있는 코드와 내 로컬 코드의 히스토리가 다르다. 다른 곳(GitHub 웹, 다른 컴퓨터)에서 코드를 수정한 적이 있다.

**해결:**
```bash
# 먼저 GitHub의 변경사항을 가져온다
git pull origin main

# 충돌이 없으면 자동 병합 후 다시 push
git push origin main
```

### 충돌 (Merge Conflict)

`git pull` 했을 때 같은 파일의 같은 부분을 서로 다르게 수정한 경우:

```
<<<<<<< HEAD
내가 수정한 코드
=======
GitHub에 있던 코드
>>>>>>> origin/main
```

**확인 방법:** 터미널에 "CONFLICT" 메시지가 나오고, 해당 파일을 열면 위 표시가 보인다.

**해결:**
```
1. 충돌난 파일을 연다
2. <<<<<<< / ======= / >>>>>>> 표시를 찾는다
3. 두 코드 중 올바른 것을 남기고 나머지를 지운다 (표시도 모두 삭제)
4. 저장 후:
   git add .
   git commit -m "resolve merge conflict"
   git push origin main
```

### 커밋할 게 없다 (nothing to commit)

```
$ git commit -m "update code"
On branch main
nothing to commit, working tree clean
```

**원인:** 파일을 수정했는데 `git add`를 안 했거나, 실제로 변경된 파일이 없다.

**확인:**
```bash
git status          # 수정된 파일이 있는지 확인
git diff            # 어떤 내용이 바뀌었는지 확인
```

### .gitignore로 인한 파일 누락

```
# .gitignore에 이렇게 적혀있으면
*.db
.env
__pycache__/
static/uploads/

# 이 파일/폴더들은 git push해도 GitHub에 올라가지 않는다
```

**자주 하는 실수:**

| 실수 | 결과 | 해결 |
|------|------|------|
| `static/` 을 .gitignore에 넣음 | HTML/CSS/JS가 배포 안 됨 | .gitignore에서 제거 |
| 새 파일을 만들고 `git add` 안 함 | 새 파일이 GitHub에 없음 | `git add 파일명` 후 커밋 |
| `.env`를 .gitignore에서 빼고 올림 | 비밀번호가 GitHub에 노출! | .gitignore에 `.env` 반드시 유지 |

### 확인하는 방법: GitHub에서 직접 확인

```
1. GitHub 저장소 페이지에 접속
2. 파일 목록을 확인
3. 로컬에 있는 파일이 GitHub에도 있는지 비교
4. 없는 파일이 있으면 → .gitignore 확인 또는 git add 누락
```

---

## 9.3 배포와 직결되는 Git 실수들

### 잘못된 브랜치 배포

```
Render 설정: main 브랜치를 배포하도록 설정됨

로컬에서:
$ git branch
  main
* develop       ← 현재 develop 브랜치에서 작업 중

$ git push origin develop   ← develop에 올림 → main에는 반영 안 됨 → 배포 안 됨!
```

**확인:**
```bash
# 현재 어떤 브랜치에 있는지 확인
git branch

# main 브랜치로 이동 후 push
git checkout main
git merge develop      # develop의 변경사항을 main에 합치기
git push origin main   # main에 push → Render 배포 시작
```

### 커밋 안 하고 push

```bash
# 파일 수정 후
git push origin main     # ← 커밋을 안 해서 변경사항이 push 안 됨!

# 올바른 순서
git add .
git commit -m "fix: update user API"
git push origin main
```

**확인:** `git status`에 "Changes not staged" 또는 "Changes to be committed"이 있으면 아직 커밋 안 한 것.

### 대용량 파일 push 실패

```
remote: error: File data.csv is 150 MB; this exceeds GitHub's file size limit of 100 MB
```

**해결:** 큰 파일은 `.gitignore`에 추가하고, 다른 방법으로 관리한다.

```gitignore
# .gitignore에 추가
*.csv
*.sqlite
*.db
uploads/
```

---

## 9.4 Git 기본 명령어 빠른 참조

### 일상적으로 쓰는 명령어

```bash
# 상태 확인 (가장 많이 쓰는 명령어)
git status

# 변경사항 확인
git diff

# 파일 추가 → 커밋 → push (배포까지의 기본 플로우)
git add .                           # 모든 변경 파일을 스테이징
git commit -m "설명 메시지"           # 커밋 생성
git push origin main                # GitHub에 올리기 → Render 자동 배포

# GitHub에서 변경사항 가져오기
git pull origin main

# 실수로 수정한 파일 되돌리기 (커밋 전에만)
git checkout -- 파일명

# 커밋 기록 보기
git log --oneline
```

### 커밋 메시지 쓰는 습관

```bash
# ❌ 나쁜 커밋 메시지
git commit -m "update"
git commit -m "fix"
git commit -m "asdf"

# ✅ 좋은 커밋 메시지 (나중에 뭘 고쳤는지 알 수 있음)
git commit -m "fix: 로그인 API 422 에러 수정"
git commit -m "feat: 사용자 목록 페이지 추가"
git commit -m "style: 메인 페이지 CSS 레이아웃 수정"
```

> **왜 중요한가?** 배포 후 에러가 나면 "언제부터 에러가 났는지" 커밋 기록을 거슬러 올라가며 찾아야 한다. 메시지가 "update"면 뭘 고쳤는지 알 수 없다.

---

## 9.5 Git 에러 디버깅 체크리스트

```
"코드를 고쳤는데 배포가 안 된다" 할 때:

□ git status: 변경 파일이 보이는가?
□ git add: 스테이징했는가?
□ git commit: 커밋했는가?
□ git push: GitHub에 올렸는가?
□ GitHub 확인: 파일이 실제로 올라갔는가?
□ Render 확인: 올바른 브랜치를 배포하고 있는가?
□ Render Deploy 로그: 빌드/시작 에러가 없는가?
```

---

## 핵심 정리

1. 배포의 전체 흐름: **코드 수정 → git add → commit → push → Render 자동 배포**
2. `git push`가 거부되면 **`git pull` 먼저** 한 후 다시 push
3. 충돌(Conflict)이 나면 파일을 열어 `<<<<<<<` 표시를 찾아 수동 해결
4. `.gitignore` 때문에 **필요한 파일이 안 올라가는 경우**가 많다 → GitHub에서 직접 확인
5. 배포가 안 되면 `git status` → GitHub 확인 → Render 로그 순서로 체크
6. 커밋 메시지를 잘 써야 **에러 원인을 추적할 때** 도움이 된다
