# XDG_LOG_HOME Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add `$XDG_LOG_HOME` and `$XDG_LOG_DIRS` as first-class base directories in the XDG Base Directory Specification.

**Architecture:** Single-file edit to `basedir/basedir-spec.xml` (DocBook XML). Four insertion points plus one text update, each as a discrete task with a commit.

**Tech Stack:** DocBook XML V4.1.2

---

## Motivation

The current spec bundles logs under `$XDG_STATE_HOME`. Separating them provides:
- Different lifecycle management (rotation, compression, pruning)
- Predictable location for log tooling (journald, logrotate, lnav)
- Safe-to-delete semantics (unlike state files apps depend on)
- Unambiguous discoverability

## New Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `$XDG_LOG_HOME` | `$HOME/.local/log` | User-specific log files |
| `$XDG_LOG_DIRS` | `/var/log` | Log file search path |

---

### Task 1: Add $XDG_LOG_HOME bullet to Basics section

**Files:**
- Modify: `basedir/basedir-spec.xml:83-84` (after `$XDG_STATE_HOME` listitem, before executable files listitem)

**Step 1: Insert new listitem**

After line 84 (the closing `</listitem>` of the `$XDG_STATE_HOME` bullet), insert:

```xml
        <listitem>
          <para>
            There is a single base directory relative to which user-specific
            log files should be written. This directory is defined by the
            environment variable <literal>$XDG_LOG_HOME</literal>.
          </para>
        </listitem>
```

**Step 2: Validate XML is well-formed**

Run: `xmllint --noout basedir/basedir-spec.xml`
Expected: no output (success)

**Step 3: Commit**

```
git add basedir/basedir-spec.xml
git commit -m "basedir: Add XDG_LOG_HOME to Basics section"
```

---

### Task 2: Add $XDG_LOG_DIRS bullet to Basics section

**Files:**
- Modify: `basedir/basedir-spec.xml` (after `$XDG_CONFIG_DIRS` listitem, before `$XDG_CACHE_HOME` listitem)

The `$XDG_CONFIG_DIRS` listitem ends around line 105 (line numbers shifted by Task 1 insertion). Insert after its closing `</listitem>`:

**Step 1: Insert new listitem**

After the `$XDG_CONFIG_DIRS` closing `</listitem>`, insert:

```xml
        <listitem>
          <para>
            There is a set of preference ordered base directories relative to
            which log files should be searched. This set of directories is defined
            by the environment variable <literal>$XDG_LOG_DIRS</literal>.
          </para>
        </listitem>
```

**Step 2: Validate XML**

Run: `xmllint --noout basedir/basedir-spec.xml`
Expected: no output (success)

**Step 3: Commit**

```
git add basedir/basedir-spec.xml
git commit -m "basedir: Add XDG_LOG_DIRS to Basics section"
```

---

### Task 3: Update $XDG_STATE_HOME description to remove logs mention

**Files:**
- Modify: `basedir/basedir-spec.xml` (the STATE_HOME itemizedlist, originally line 158)

**Step 1: Replace the first listitem text**

Change:

```xml
        <listitem><para>actions history (logs, history, recently used files, …)</para></listitem>
```

To:

```xml
        <listitem><para>actions history (history, recently used files, …).
        Log files should be stored in <literal>$XDG_LOG_HOME</literal> instead.</para></listitem>
```

**Step 2: Validate XML**

Run: `xmllint --noout basedir/basedir-spec.xml`
Expected: no output (success)

**Step 3: Commit**

```
git add basedir/basedir-spec.xml
git commit -m "basedir: Direct log files to XDG_LOG_HOME instead of XDG_STATE_HOME"
```

---

### Task 4: Add $XDG_LOG_HOME and $XDG_LOG_DIRS to Environment variables section

**Files:**
- Modify: `basedir/basedir-spec.xml` (Environment variables section)

**Step 1: Insert $XDG_LOG_HOME paragraphs**

After the `$XDG_STATE_HOME` itemizedlist closing `</para>` (originally line 162, shifted by earlier edits), insert:

```xml
    <para>
      <literal>$XDG_LOG_HOME</literal> defines the base directory relative to
      which user-specific log files should be stored. If
      <literal>$XDG_LOG_HOME</literal> is either not set or empty, a default equal to
      <literal>$HOME</literal>/.local/log should be used.
    </para>
    <para>
      Log files are informational records of application activity intended for
      debugging, auditing, or monitoring. They are append-oriented and may grow
      without bound. Deleting log files MUST NOT affect the correctness or
      functionality of applications.
    </para>
    <para>
      Applications SHOULD organize log files into subdirectories of
      <literal>$XDG_LOG_HOME</literal> named after the application. Applications
      SHOULD document their log retention expectations.
    </para>
```

**Step 2: Insert $XDG_LOG_DIRS paragraphs**

After the `$XDG_CONFIG_DIRS` default value paragraph (originally line 200-201), insert:

```xml
    <para>
      <literal>$XDG_LOG_DIRS</literal> defines the preference-ordered set of
      base directories to search for log files in addition to the
      <literal>$XDG_LOG_HOME</literal> base directory.
      The directories in <literal>$XDG_LOG_DIRS</literal> should be separated
      with the separator used for <literal>$PATH</literal> on the platform
      (typically this is a colon <literal>:</literal>).
    </para>
    <para>
      If <literal>$XDG_LOG_DIRS</literal> is either not set or empty, a value equal to
      /var/log should be used.
    </para>
```

**Step 3: Update the precedence paragraph**

The existing paragraph (originally lines 202-212) mentions DATA and CONFIG precedence. Append a new sentence to it:

```xml
      The base directory defined
      by <literal>$XDG_LOG_HOME</literal> is considered more important than
      any of the base directories defined by <literal>$XDG_LOG_DIRS</literal>.
```

**Step 4: Validate XML**

Run: `xmllint --noout basedir/basedir-spec.xml`
Expected: no output (success)

**Step 5: Commit**

```
git add basedir/basedir-spec.xml
git commit -m "basedir: Define XDG_LOG_HOME and XDG_LOG_DIRS environment variables"
```

---

### Task 5: Add log file referencing guidance

**Files:**
- Modify: `basedir/basedir-spec.xml` (Referencing section)

**Step 1: Insert log referencing block**

After the `$XDG_CONFIG_DIRS` referencing block (originally ending at line 324), insert:

```xml
    <para>
      Specifications may reference this specification by specifying the
      location of a log file as
      <literal>$XDG_LOG_DIRS</literal>/subdir/filename. This implies that:
      <itemizedlist>
        <listitem>
          <para>
            Such file should be installed to <literal>$logdir</literal>/subdir/filename
            with <literal>$logdir</literal> defaulting to /var/log.
          </para>
        </listitem>
        <listitem>
          <para>
            A user-specific version of the log file may be created in
            <literal>$XDG_LOG_HOME</literal>/subdir/filename, taking into
            account the default value for <literal>$XDG_LOG_HOME</literal> if
            <literal>$XDG_LOG_HOME</literal> is not set.
          </para>
        </listitem>
        <listitem>
          <para>
            Lookups of the log file should search for ./subdir/filename relative to
            all base directories specified by <literal>$XDG_LOG_HOME</literal> and
            <literal>$XDG_LOG_DIRS</literal> . If an environment
            variable is either not set or empty, its default value as defined by this specification
            should be used instead.
          </para>
        </listitem>
      </itemizedlist>
    </para>
```

**Step 2: Update the multi-base-directory behavior paragraph**

Change (originally lines 344-345):

```xml
      A specification that refers to <literal>$XDG_DATA_DIRS</literal> or
      <literal>$XDG_CONFIG_DIRS</literal> should define what the behaviour
```

To:

```xml
      A specification that refers to <literal>$XDG_DATA_DIRS</literal>,
      <literal>$XDG_CONFIG_DIRS</literal>, or
      <literal>$XDG_LOG_DIRS</literal> should define what the behaviour
```

**Step 3: Validate XML**

Run: `xmllint --noout basedir/basedir-spec.xml`
Expected: no output (success)

**Step 4: Commit**

```
git add basedir/basedir-spec.xml
git commit -m "basedir: Add log file referencing guidance for XDG_LOG_DIRS"
```

---

### Task 6: Bump version

**Files:**
- Modify: `basedir/basedir-spec.xml:7-8` (releaseinfo and pubdate)

**Step 1: Update version and date**

Change:

```xml
    <releaseinfo>Version 0.8</releaseinfo>
    <pubdate>08th May 2021</pubdate>
```

To:

```xml
    <releaseinfo>Version 0.9</releaseinfo>
    <pubdate>24th February 2026</pubdate>
```

**Step 2: Validate XML**

Run: `xmllint --noout basedir/basedir-spec.xml`
Expected: no output (success)

**Step 3: Commit**

```
git add basedir/basedir-spec.xml
git commit -m "basedir: Bump to version 0.9 for XDG_LOG_HOME addition"
```
