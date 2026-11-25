# iOS Release Checklist

## One-time setup

- [ ] Apple Developer Program active
- [ ] App ID created in Developer portal
- [ ] Bundle ID matches the selected iOS release configuration
- [ ] Distribution certificate + App Store provisioning profile
- [ ] App Store Connect app record created
- [ ] For projects with flavors, the shared release scheme matches the project's configuration

## Per release

- [ ] Version/build bumped in `pubspec.yaml` and Xcode
- [ ] `flutter build ipa` with the project's release flavor and define arguments when configured
- [ ] Archive validates on Organizer
- [ ] Upload to App Store Connect succeeds
- [ ] Export compliance answered
- [ ] Screenshots match current UI
- [ ] Privacy nutrition labels match `privacy-questionnaire.md`
- [ ] Review notes include demo account if login required

## Post-rejection

1. Log rejection reason in `app-store-submission.md`
2. Classify: metadata | compliance | bug | guideline
3. Route: bug → Phase 5/6; metadata → update submission only
