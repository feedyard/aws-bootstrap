# Using APP_NAME Securely

This document discusses using and configuring APP_NAME is a secure manner.

## Security related use or configuration

### Known Vulnerabilities

### Reporting vulnerabilities  (or possibly the community edition of HackerOne)

Please email reports about any security related issues you find to
`security@org_name.org`. This mail is delivered to a small security team. Your
email will be acknowledged within one business day, and you'll receive a more
detailed response to your email within 7 days indicating the next steps in
handling your report. For critical problems, you may encrypt your report (see
below).

Please use a descriptive subject line for your report email. After the initial
reply to your report, the security team will endeavor to keep you informed of
the progress being made towards a fix and announcement.

In addition, please include the following information along with your report:

* Your name and affiliation (if any).
* A description of the technical details of the vulnerabilities. It is very
  important to let us know how we can reproduce your findings.
* An explanation who can exploit this vulnerability, and what they gain when
  doing so -- write an attack scenario. This will help us evaluate your report
  quickly, especially if the issue is complex.
* Whether this vulnerability public or known to third parties. If it is, please
  provide details.

If you believe that an existing (public) issue is security-related, please send
an email to `security@org_name.org`. The email should include the issue ID and
a short description of why it should be handled according to this security
policy.

Once an issue is reported, Org_name uses the following disclosure process:

* When a report is received, we confirm the issue and determine its severity.
* If we know of specific third-party services or software based on TensorFlow
  that require mitigation before publication, those projects will be notified.
* An advisory is prepared (but not published) which details the problem and
  steps for mitigation.
* Wherever possible, fixes are prepared for the last minor release of the two
  latest major releases, as well as the master branch. We will attempt to
  commit these fixes as soon as possible, and as close together as
  possible.
* Patch releases are published for all fixed released versions, a
  notification is sent to discuss@tensorflow.org, and the advisory is published.

Past security advisories are listed below. We credit reporters for identifying
security issues, although we keep your name confidential if you request it.

#### Encryption key for `security@org_name.org`

If your disclosure is extremely sensitive, you may choose to encrypt your
report using the key below. Please only use this for critical security
reports.

```
-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBFpqdzwBCADTeAHLNEe9Vm77AxhmGP+CdjlY84O6DouOCDSq00zFYdIU/7aI
LjYwhEmDEvLnRCYeFGdIHVtW9YrVktqYE9HXVQC7nULU6U6cvkQbwHCdrjaDaylP
aJUXkNrrxibhx9YYdy465CfusAaZ0aM+T9DpcZg98SmsSml/HAiiY4mbg/yNVdPs
SEp/Ui4zdIBNNs6at2gGZrd4qWhdM0MqGJlehqdeUKRICE/mdedXwsWLM8AfEA0e
OeTVhZ+EtYCypiF4fVl/NsqJ/zhBJpCx/1FBI1Uf/lu2TE4eOS1FgmIqb2j4T+jY
e+4C8kGB405PAC0n50YpOrOs6k7fiQDjYmbNABEBAAG0LVRlbnNvckZsb3cgU2Vj
dXJpdHkgPHNlY3VyaXR5QHRlbnNvcmZsb3cub3JnPokBTgQTAQgAOBYhBEkvXzHm
SEp/Ui4zdIBNNs6at2gGZrd4qWhdM0MqGJlehqdeUKRICE/mdedXwsWLM8AfEA0e
OeTVhZ+EtYCypiF4fVl/NsqJ/zhBJpCx/1FBI1Uf/lu2TE4eOS1FgmIqb2j4T+jY
o+X2dlPqBSqMG3bFuTrrcwjr9w1V8HkNuzzOJvCm1CJVKaxMzPuXhBq5+DeT67+a
T/wK1L2R1bF0gs7Pp40W3np8iAFEh8sgqtxXvLGJLGDZ1Lnfdprg3HciqaVAiTum
HBFwszszZZ1wAnKJs5KVteFN7GSSng3qBcj0E0ql2nPGEqCVh+6RG/TU5C8gEsEf
3DX768M4okmFDKTzLNBm+l08kkBFt+P43rNK8dyC4PXk7yJa93SmS/dlK6DZ16Yw
2FS1StiZSVqygTW59rM5XNwdhKVXy2mf/RtNSr84gSi5AQ0EWmp3PAEIALInfBLR
SEp/Ui4zdIBNNs6at2gGZrd4qWhdM0MqGJlehqdeUKRICE/mdedXwsWLM8AfEA0e
OeTVhZ+EtYCypiF4fVl/NsqJ/zhBJpCx/1FBI1Uf/lu2TE4eOS1FgmIqb2j4T+jY
osdG2XnnTHOOEFbEUeWOwR/zT0QRaGGknoy2pc4doWcJptqJIdTl1K8xyBieik/b
nSoClqQdZJa4XA3H9G+F4NmoZGEguC5GGb2P9NHYAJ3MLHBHywZip8g9oojIwda+
OCLL4UPEZ89cl0EyhXM0nIAmGn3Chdjfu3ebF0SeuToGN8E1goUs3qSE77ZdzIsR
BzZSDFrgmZH+uP0AEQEAAYkBNgQYAQgAIBYhBEkvXzHmgOJBnwP4Wxnef3wVoM2y
BQJaanc8AhsMAAoJEBnef3wVoM2yX4wIALcYZbQhSEzCsTl56UHofze6C3QuFQIH
SEp/Ui4zdIBNNs6at2gGZrd4qWhdM0MqGJlehqdeUKRICE/mdedXwsWLM8AfEA0e
OeTVhZ+EtYCypiF4fVl/NsqJ/zhBJpCx/1FBI1Uf/lu2TE4eOS1FgmIqb2j4T+jY
7Obq96Jb/cPRxk8jKUu2rqC/KDrkFDtAtjdIHh6nbbQhFuaRuWntISZgpIJxd8Bt
Gwi0imUVd9m9wZGuTbDGi6YTNk0GPpX5OMF5hjtM/objzTihSw9UN+65Y/oSQM81
v//Fw6ZeY+HmRDFdirjD7wXtIuER4vqCryIqR6Xe9X8oJXz9L/Jhslc=
=CDME
-----END PGP PUBLIC KEY BLOCK-----
```
