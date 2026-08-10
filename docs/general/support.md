# Support

!!! overview "On this Page"
      - What to check before you get in touch
      - How to reach the eResearch Support team, and what each channel is best for
      - What to include so we can help on the first reply
      - Requests that have their own form
      - Best practices for providing an example test dataset

## Before You Contact Us

Three quick checks answer most questions, and none of them take long:

  * **Is it already answered?** The [Frequently Asked Questions](faq/index.md) cover the
    problems we are asked about most often, including
    [Why Is My Job Not Starting?](faq/job_start_time.md) and
    [Why Did My Job Fail?](faq/slurm_job_failures.md).
  * **Is the cluster busy rather than broken?** A job sitting in `PENDING` is usually waiting
    for resources, not stuck. [Cluster Traffic](../getting_started/current_utilisation.md)
    shows what is currently in use.
  * **Is it your job or the cluster?** If the same job worked yesterday and fails today,
    say so — that is one of the most useful things you can tell us.

## How to Reach Us

Table: Where to send what, and what comes back

| Channel | Best for | You get |
|---|---|---|
| **{{ support_email }}** | Anything at all, and always for continuing a conversation already under way | A reply by email |
| **[Research Computing Teams channel](https://teams.microsoft.com/l/team/19%3AwY-QPCGhXz_nHt4-0C7Ltz7gdVAmE_1fDfmgFO4bnHs1%40thread.tacv2/conversations?groupId=de270594-2da5-4354-b319-57f8894c89f3&tenantId=0225efc5-78fe-4928-b157-9ef24809e9ba)** | Quick questions, and answers from other cluster users as well as from us | A conversation |

{# To publish the triage form: set `support_form` in mkdocs.yml, uncomment the block below,
   and add this row to the top of the table above. The row cannot live in a commented block
   inside the table itself — stripping it leaves a blank line, which ends the table early.

| **[Support form]({{ support_form }}){ target="_blank" }** | A new problem or request — the form asks for the details we need up front | A reply by email |

The support form is the quickest way to send us a new problem, because it asks for the job ID
and the error output rather than leaving you to guess what we need.

[Contact Support :material-arrow-right:]({{ support_form }}){ .md-button .md-button--primary target="_blank" }

Submitting the form sends your request to the eResearch Support team and you will get a reply
by email. There is no reference number to quote — the email thread *is* the record. If you have
not heard back and want to add something, reply to your own message or email the address above
rather than submitting the form a second time.
#}

Email the eResearch Support team at **{{ support_email }}**. Most of us are not scientific or
domain experts in your field, so the more you can tell us about what you were trying to do, the
faster we can be useful.

![Support graphic](../assets/images/support_graphic1.png){ width="800" .left }

## What to Include

Whichever way you get in touch, these are what let us start work rather than start with
questions:

  * **The job ID**, for anything involving a job. That alone tells us the node, the partition,
    the resources it asked for and how it ended.
  * **The exact error message**, copied as text rather than a screenshot. Screenshots are
    genuinely useful for graphical applications, but text output that we can search and paste
    back is far easier to work with.
  * **The commands or job script** you ran, and how you submitted them.
  * **What you expected to happen**, and what happened instead.
  * **Whether it has ever worked** — first attempt, used to work, or intermittent.
  * **An example test dataset**, if the problem needs data to reproduce. See
    [best practices](#best-practices-for-providing-an-example-test-dataset) below.

### Diagnostics to Paste In

Running these and pasting the output covers most of the list above in one go.

!!! terminal

    ```bash
    # For a job problem — replace <jobid> with the job you are asking about
    sacct -j <jobid> -o JobID,JobName,Partition,State,ExitCode,Elapsed,ReqMem,MaxRSS,NodeList
    seff <jobid>

    # For a software or environment problem
    hostname
    module list
    which <command>
    ```

You do not need to interpret the output — send it as it comes. If you would like to read it
yourself, [Job Efficiency](../getting_started/running/efficiency.md) explains what `seff` and
`sacct` are telling you.

## Requests With Their Own Form

Some requests go through a form rather than an email, so that they reach the right people with
the right details:

[Request an Account :material-arrow-right:](../getting_started/access/signup.md){ .md-button }
[Request Storage :material-arrow-right:](../storage/storage_request.md){ .md-button }
[Request Globus Access :material-arrow-right:](../storage/data_transfer/globus_registration.md){ .md-button }

## Best Practices for Providing an Example Test Dataset

When a problem needs data to reproduce, a small example saves everyone time:

  * **Keep it small.** Use the smallest dataset that still reproduces the issue — that makes it
    faster to diagnose for us, and often clearer for you.
  * **Make it self-contained.** Include the input files, the script and anything else needed to
    run it, so we are not chasing missing pieces.
  * **Use a standard format.** A text file or a widely-supported binary format is easiest for us
    to open.
  * **Leave out sensitive data.** Remove anything confidential or personally identifying before
    sharing it, and tell us if the real data has properties the sample does not.

!!! related-pages "What's next?"
      - Looking for something else? See the [Frequently Asked Questions](faq/index.md).
      - New to the cluster? Start with [Cluster Overview](../getting_started/overview.md).
      - [Home Page](../index.md)
