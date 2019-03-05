describe('Goal Management System End to End Testing', function () {
  beforeEach(function () {
    browser.get('http://localhost:4200/teacher')
  })
  var CreateGoalButton = element(by.buttonText('Create Goal'))
  var GoalTitle = element(by.css("input[placeholder = 'Goal Title']"))
  var Description = element(by.css("input[class = 'description']"))
  var GoalList = element(by.css("div[class = 'w3-container w3-card w3-white w3-margin-bottom']"))
  var GoalCard = element(by.css('div'))
  var GoalButton = element(by.css('a[ng-reflect-router-link="/student/goals"]'))
  var AssignGoal = element(by.buttonText('Assign Goals'))
  var GoalHistory = element(by.buttonText('Goal History'))
  var GoalHistoryCard = element(by.css("div[class = 'w3-container']"))
  var LoginButton = element(by.buttonText('Login'))

  it('Should add a goal to the thicc list', function () {
    GoalTitle.sendKeys('Test Goal Title asfasdf')
    Description.sendKeys('Test Goal Description David is dumb')
    CreateGoalButton.click()
    expect(GoalList.getText())
      .toContain('Test Goal Title asfasdf\nDescription:\nTest Goal Description David is dumb\nDue Date:\nDelete');
  })
  // TODO: Should differentiate between teacher and student
  // TODO: Should assign a goal to a student
  it('Should assign a goal to a student', function () {
    GoalButton.click()
    element(by.css('input[class = INSERT_STUDENT_NAME_HERE]')).click()
    AssignGoal.click()
    expect(GoalCard.getText())
      .toContain('Test Goal Title asfasdf\nDescription:\nTest Goal Description:\n David is dumb Due Date:\nDelete\nSTUDENT_ONE_HERE')
  })
  it('Should assign multiple students a goal', function () {
    GoalButton.click()
    element(by.css('input[class = INSERT_STUDENT_NAME_HERE]')).click()
    element(by.css('input[class = INSERT_STUDENT_NAME_HERE')).click()
    AssignGoal.click()
    expect(GoalCard.getText())
      .toContain('Test Goal Title asfasdf\nDescription:\nTest Goal Description:\n David is dumb Due Date:\nDelete\nSTUDENT_ONE_HERE\nSTUDENT_TWO_HERE')
  })
  // TODO: Should return an error when no students are assigned
  it('Should return an error when no students are assigned', function () {
    var EC = protractor.ExpectedConditions
    GoalButton.click()
    AssignGoal.click()
    browser.wait(EC.alertIsPresent(), 5000)
  });
  // TODO: Empty Goal Text Error
  it('Should return an error if no Goal Name is entered', function () {
    var EC = protractor.ExpectedConditions
    Description.sendKeys('Test Goal Description David is dumb')
    CreateGoalButton.click()
    browser.wait(EC.alertIsPresent(), 5000)
  })
  // TODO: Goal History Updates Correctly
  it('Should update Goal History Correctly', function () {
    GoalTitle.sendKeys('Test Goal History')
    Description.sendKeys('Test Goal History Description')
    CreateGoalButton.click()
    GoalHistory.click()
    expect(GoalHistoryCard.getText()).toContain('Test Goal History\nTest Goal History Description')
  })
  //  TODO: Google Login returns individual goals
  it('Should return students who login', function () {
    GoalTitle.sendKeys('Test Goal Login')
    Description.sendKeys('Test Goal Login Description')
    CreateGoalButton.click()
    element(by.css('input[class = INSERT_STUDENT_NAME_HERE]')).click()
    element(by.css('input[class = INSERT_STUDENT_NAME_HERE')).click()
    AssignGoal.click()
    LoginButton.click()
    // login, go to home
    expect(GoalHistoryCard.getText()).toContain('Test Goal History\nTest Goal History Description');
  })
})
