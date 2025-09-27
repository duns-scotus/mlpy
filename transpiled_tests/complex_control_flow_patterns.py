"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

from mlpy.stdlib.string_bridge import string as ml_string

from mlpy.stdlib.datetime_bridge import datetime as ml_datetime

# WARNING: Import 'regex' requires security review
# import regex

def complex_nested_conditions():
    print('=== Complex Nested Conditional Structures ===')
    def evaluate_loan_application(credit_score, income, debt_ratio, employment_years):
        status = 'unknown'
        interest_rate = 0.0
        reason = ''
        if (credit_score >= 800):
            if (income >= 100000):
                if (debt_ratio < 0.2):
                    if (employment_years >= 2):
                        status = 'approved'
                        interest_rate = 3.5
                        reason = 'Excellent credit and financial profile'
                    else:
                        status = 'conditional'
                        interest_rate = 4.0
                        reason = 'Excellent credit but limited employment history'
                elif (debt_ratio < 0.3):
                    status = 'conditional'
                    interest_rate = 4.2
                    reason = 'Excellent credit but moderate debt ratio'
                else:
                    status = 'declined'
                    reason = 'High debt ratio despite excellent credit'
            elif (income >= 75000):
                if ((debt_ratio < 0.25) and (employment_years >= 3)):
                    status = 'approved'
                    interest_rate = 3.8
                    reason = 'Good income and employment stability'
                else:
                    status = 'conditional'
                    interest_rate = 4.5
                    reason = 'Needs review for income/stability'
            else:
                status = 'conditional'
                interest_rate = 5.0
                reason = 'High credit score but lower income'
        elif (credit_score >= 700):
            if (((income >= 80000) and (debt_ratio < 0.25)) and (employment_years >= 2)):
                status = 'approved'
                interest_rate = 4.2
                reason = 'Good credit with strong financial indicators'
            elif ((income >= 60000) and (debt_ratio < 0.3)):
                status = 'conditional'
                interest_rate = 5.0
                reason = 'Good credit, moderate financial profile'
            else:
                status = 'declined'
                reason = 'Good credit but insufficient income or high debt'
        elif (credit_score >= 600):
            if (((income >= 70000) and (debt_ratio < 0.2)) and (employment_years >= 5)):
                status = 'conditional'
                interest_rate = 6.0
                reason = 'Fair credit compensated by strong financials'
            else:
                status = 'declined'
                reason = 'Fair credit with inadequate compensation factors'
        else:
            status = 'declined'
            reason = 'Credit score too low for approval'
        return {'status': status, 'interest_rate': interest_rate, 'reason': reason, 'application': {'credit_score': credit_score, 'income': income, 'debt_ratio': debt_ratio, 'employment_years': employment_years}}
    applications = [{'credit': 850, 'income': 120000, 'debt': 0.15, 'employment': 5}, {'credit': 780, 'income': 90000, 'debt': 0.35, 'employment': 3}, {'credit': 720, 'income': 65000, 'debt': 0.28, 'employment': 1}, {'credit': 650, 'income': 85000, 'debt': 0.18, 'employment': 8}, {'credit': 580, 'income': 95000, 'debt': 0.15, 'employment': 10}]
    i = 0
    while (i < applications['length']()):
        app = applications[i]
        result = evaluate_loan_application(app['credit'], app['income'], app['debt'], app['employment'])
        print((str((str((str((str((str('Application ') + str((i + 1)))) + str(': '))) + str(result['status']))) + str(' - '))) + str(result['reason'])))
        if ((result['status'] == 'approved') or (result['status'] == 'conditional')):
            print((str((str('  Interest Rate: ') + str(result['interest_rate']))) + str('%')))
        i = (i + 1)
    return applications

def advanced_loop_patterns():
    print('\\n=== Advanced Loop Control Patterns ===')
    def find_matrix_patterns(matrix):
        rows = matrix['length']()
        cols = matrix[0]['length']()
        patterns_found = []
        i = 0
        while (i < (rows - 2)):
            j = 0
            while (j < (cols - 2)):
                diagonal_sum = ((matrix[i][j] + matrix[(i + 1)][(j + 1)]) + matrix[(i + 2)][(j + 2)])
                anti_diagonal_sum = ((matrix[i][(j + 2)] + matrix[(i + 1)][(j + 1)]) + matrix[(i + 2)][j])
                if (diagonal_sum == 15):
                    patterns_found[patterns_found['length']()] = {'type': 'diagonal', 'position': {'row': i, 'col': j}, 'sum': diagonal_sum}
                if (anti_diagonal_sum == 15):
                    patterns_found[patterns_found['length']()] = {'type': 'anti_diagonal', 'position': {'row': i, 'col': j}, 'sum': anti_diagonal_sum}
                j = (j + 1)
            i = (i + 1)
        return patterns_found
    test_matrix = [[1, 2, 3, 4, 5], [2, 4, 6, 8, 1], [3, 6, 9, 2, 4], [4, 8, 2, 5, 7], [5, 1, 4, 7, 3]]
    patterns = find_matrix_patterns(test_matrix)
    print('Matrix pattern search results:')
    print((str('Patterns found: ') + str(patterns['length']())))
    k = 0
    while (k < patterns['length']()):
        pattern = patterns[k]
        print((str((str((str((str((str((str((str('  ') + str(pattern['type']))) + str(' at ('))) + str(pattern['position']['row']))) + str(', '))) + str(pattern['position']['col']))) + str(') - Sum: '))) + str(pattern['sum'])))
        k = (k + 1)
    def collatz_conjecture(n):
        sequence = [n]
        steps = 0
        max_steps = 1000
        while ((n != 1) and (steps < max_steps)):
            if ((n % 2) == 0):
                n = (n / 2)
            else:
                n = ((3 * n) + 1)
            sequence[sequence['length']()] = n
            steps = (steps + 1)
        return {'original': sequence[0], 'sequence': sequence, 'steps': steps, 'converged': (n == 1)}
    test_numbers = [3, 5, 7, 12, 27]
    print('\\nCollatz Conjecture Results:')
    l = 0
    while (l < test_numbers['length']()):
        num = test_numbers[l]
        result = collatz_conjecture(num)
        print((str((str((str((str((str('Starting with ') + str(num))) + str(': '))) + str(result['steps']))) + str(' steps, converged: '))) + str(result['converged'])))
        print((str('  First 10 values: ') + str(ml_string.substring(result['sequence'], 0, 10))))
        l = (l + 1)
    return {'matrix_patterns': patterns, 'collatz_results': test_numbers}

def complex_switch_patterns():
    print('\\n=== Complex Switch-Case Equivalent Patterns ===')
    def process_state_machine(events):
        state = 'idle'
        processed_events = []
        state_history = ['idle']
        error_count = 0
        max_errors = 3
        i = 0
        while ((i < events['length']()) and (error_count < max_errors)):
            event = events[i]
            old_state = state
            action_taken = ''
            if (state == 'idle'):
                if (event == 'start'):
                    state = 'initializing'
                    action_taken = 'Beginning initialization process'
                elif (event == 'shutdown'):
                    state = 'shutdown'
                    action_taken = 'Shutting down from idle'
                elif (event == 'reset'):
                    action_taken = 'Already in idle state'
                else:
                    error_count = (error_count + 1)
                    action_taken = (str('Invalid event in idle state: ') + str(event))
            elif (state == 'initializing'):
                if (event == 'init_complete'):
                    state = 'ready'
                    action_taken = 'Initialization completed successfully'
                elif (event == 'init_error'):
                    state = 'error'
                    action_taken = 'Initialization failed'
                    error_count = (error_count + 1)
                elif (event == 'cancel'):
                    state = 'idle'
                    action_taken = 'Initialization cancelled'
                else:
                    error_count = (error_count + 1)
                    action_taken = (str('Invalid event during initialization: ') + str(event))
            elif (state == 'ready'):
                if (event == 'execute'):
                    state = 'running'
                    action_taken = 'Starting execution'
                elif (event == 'configure'):
                    state = 'configuring'
                    action_taken = 'Entering configuration mode'
                elif (event == 'shutdown'):
                    state = 'shutdown'
                    action_taken = 'Shutting down from ready'
                elif (event == 'reset'):
                    state = 'idle'
                    action_taken = 'Reset to idle state'
                else:
                    error_count = (error_count + 1)
                    action_taken = (str('Invalid event in ready state: ') + str(event))
            elif (state == 'running'):
                if (event == 'pause'):
                    state = 'paused'
                    action_taken = 'Execution paused'
                elif (event == 'complete'):
                    state = 'completed'
                    action_taken = 'Execution completed successfully'
                elif (event == 'error'):
                    state = 'error'
                    action_taken = 'Runtime error occurred'
                    error_count = (error_count + 1)
                elif (event == 'stop'):
                    state = 'ready'
                    action_taken = 'Execution stopped, returning to ready'
                else:
                    error_count = (error_count + 1)
                    action_taken = (str('Invalid event during execution: ') + str(event))
            elif (state == 'paused'):
                if (event == 'resume'):
                    state = 'running'
                    action_taken = 'Execution resumed'
                elif (event == 'stop'):
                    state = 'ready'
                    action_taken = 'Stopped from pause, returning to ready'
                elif (event == 'reset'):
                    state = 'idle'
                    action_taken = 'Reset from pause to idle'
                else:
                    error_count = (error_count + 1)
                    action_taken = (str('Invalid event in paused state: ') + str(event))
            elif (state == 'configuring'):
                if (event == 'config_save'):
                    state = 'ready'
                    action_taken = 'Configuration saved, returning to ready'
                elif (event == 'config_cancel'):
                    state = 'ready'
                    action_taken = 'Configuration cancelled'
                else:
                    error_count = (error_count + 1)
                    action_taken = (str('Invalid event in configuration: ') + str(event))
            elif (state == 'completed'):
                if (event == 'reset'):
                    state = 'idle'
                    action_taken = 'Reset from completed to idle'
                elif (event == 'restart'):
                    state = 'ready'
                    action_taken = 'Restarted from completed'
                else:
                    error_count = (error_count + 1)
                    action_taken = (str('Invalid event in completed state: ') + str(event))
            elif (state == 'error'):
                if (event == 'reset'):
                    state = 'idle'
                    action_taken = 'Reset from error to idle'
                    error_count = 0
                elif (event == 'retry'):
                    state = 'initializing'
                    action_taken = 'Retrying from error state'
                else:
                    error_count = (error_count + 1)
                    action_taken = (str('Additional error event: ') + str(event))
            elif (state == 'shutdown'):
                action_taken = (str('System is shut down, ignoring event: ') + str(event))
            processed_events[processed_events['length']()] = {'event': event, 'old_state': old_state, 'new_state': state, 'action': action_taken, 'error_count': error_count}
            if (old_state != state):
                state_history[state_history['length']()] = state
            i = (i + 1)
        return {'final_state': state, 'error_count': error_count, 'state_history': state_history, 'processed_events': processed_events, 'max_errors_reached': (error_count >= max_errors)}
    test_events = ['start', 'init_complete', 'execute', 'pause', 'resume', 'complete', 'reset', 'start', 'init_error', 'retry', 'init_complete', 'configure', 'config_save', 'invalid_event', 'execute', 'error', 'reset']
    machine_result = process_state_machine(test_events)
    print('State Machine Processing Results:')
    print((str('Final state: ') + str(machine_result['final_state'])))
    print((str('Total errors: ') + str(machine_result['error_count'])))
    print((str('State progression: ') + str(machine_result['state_history'])))
    print('\\nEvent processing details:')
    j = 0
    while ((j < machine_result['processed_events']['length']()) and (j < 10)):
        event_info = machine_result['processed_events'][j]
        print((str((str((str((str((str('  ') + str(event_info['old_state']))) + str(' --['))) + str(event_info['event']))) + str(']--> '))) + str(event_info['new_state'])))
        j = (j + 1)
    return machine_result

def complex_conditional_expressions():
    print('\\n=== Complex Conditional Expressions ===')
    def evaluate_job_candidate(candidate):
        meets_education = (candidate['education_level'] >= 3)
        meets_experience = (candidate['years_experience'] >= 2)
        meets_skills = (candidate['technical_skills'] >= 7)
        meets_communication = (candidate['communication_score'] >= 8)
        meets_culture_fit = (candidate['culture_fit_score'] >= 7)
        in_salary_range = (candidate['expected_salary'] <= 120000)
        is_qualified = ((meets_education and meets_experience) and (meets_skills or meets_communication))
        is_excellent = ((((meets_education and meets_experience) and meets_skills) and meets_communication) and meets_culture_fit)
        is_affordable = (in_salary_range or ((candidate['expected_salary'] <= 140000) and is_excellent))
        final_decision = ''
        if (is_excellent and is_affordable):
            final_decision = 'hire_immediately'
        elif ((is_qualified and is_affordable) and meets_culture_fit):
            final_decision = 'hire_conditionally'
        elif ((is_qualified and is_affordable) and is_excellent):
            final_decision = 'negotiate_salary'
        elif (is_qualified and meets_culture_fit):
            final_decision = 'second_interview'
        elif (meets_education and meets_experience):
            final_decision = 'consider_for_training'
        else:
            final_decision = 'decline'
        return {'candidate_id': candidate['id'], 'decision': final_decision, 'criteria_met': {'education': meets_education, 'experience': meets_experience, 'skills': meets_skills, 'communication': meets_communication, 'culture_fit': meets_culture_fit, 'salary': is_affordable}, 'overall_scores': {'qualified': is_qualified, 'excellent': is_excellent, 'affordable': is_affordable}}
    candidates = [{'id': 1, 'education_level': 4, 'years_experience': 5, 'technical_skills': 9, 'communication_score': 8, 'culture_fit_score': 9, 'expected_salary': 95000}, {'id': 2, 'education_level': 3, 'years_experience': 3, 'technical_skills': 6, 'communication_score': 9, 'culture_fit_score': 8, 'expected_salary': 110000}, {'id': 3, 'education_level': 4, 'years_experience': 8, 'technical_skills': 10, 'communication_score': 7, 'culture_fit_score': 6, 'expected_salary': 150000}, {'id': 4, 'education_level': 2, 'years_experience': 1, 'technical_skills': 8, 'communication_score': 7, 'culture_fit_score': 9, 'expected_salary': 75000}, {'id': 5, 'education_level': 3, 'years_experience': 4, 'technical_skills': 5, 'communication_score': 6, 'culture_fit_score': 5, 'expected_salary': 130000}]
    print('Job candidate evaluation results:')
    k = 0
    while (k < candidates['length']()):
        candidate = candidates[k]
        evaluation = evaluate_job_candidate(candidate)
        print((str((str((str('Candidate ') + str(evaluation['candidate_id']))) + str(': '))) + str(evaluation['decision'])))
        if ((evaluation['decision'] == 'hire_immediately') or (evaluation['decision'] == 'hire_conditionally')):
            print((str((str((str((str((str('  Strong candidate - Education: ') + str(evaluation['criteria_met']['education']))) + str(', Skills: '))) + str(evaluation['criteria_met']['skills']))) + str(', Culture: '))) + str(evaluation['criteria_met']['culture_fit'])))
        k = (k + 1)
    return candidates

def advanced_guard_clauses():
    print('\\n=== Advanced Guard Clauses and Early Returns ===')
    def process_financial_transaction(transaction):
        if (transaction == None):
            return {'success': False, 'error': 'Transaction is null', 'code': 'NULL_INPUT'}
        if ((transaction['amount'] == None) or (transaction['amount'] <= 0)):
            return {'success': False, 'error': 'Invalid transaction amount', 'code': 'INVALID_AMOUNT'}
        if ((transaction['from_account'] == None) or (ml_string.length(transaction['from_account']) == 0)):
            return {'success': False, 'error': 'Source account required', 'code': 'MISSING_FROM_ACCOUNT'}
        if ((transaction['to_account'] == None) or (ml_string.length(transaction['to_account']) == 0)):
            return {'success': False, 'error': 'Destination account required', 'code': 'MISSING_TO_ACCOUNT'}
        if (transaction['from_account'] == transaction['to_account']):
            return {'success': False, 'error': 'Cannot transfer to same account', 'code': 'SAME_ACCOUNT'}
        if (transaction['amount'] > 50000):
            if ((transaction['authorization_code'] == None) or (ml_string.length(transaction['authorization_code']) < 6)):
                return {'success': False, 'error': 'Large transaction requires authorization code', 'code': 'AUTH_REQUIRED'}
        if (((transaction['currency'] != 'USD') and (transaction['currency'] != 'EUR')) and (transaction['currency'] != 'GBP')):
            return {'success': False, 'error': (str('Unsupported currency: ') + str(transaction['currency'])), 'code': 'UNSUPPORTED_CURRENCY'}
        from_balance = get_account_balance(transaction['from_account'])
        if (from_balance['error'] != None):
            return {'success': False, 'error': (str('Cannot verify source account: ') + str(from_balance['error'])), 'code': 'ACCOUNT_ERROR'}
        if (from_balance['balance'] < transaction['amount']):
            return {'success': False, 'error': 'Insufficient funds', 'code': 'INSUFFICIENT_FUNDS'}
        to_account_exists = verify_account_exists(transaction['to_account'])
        if to_account_exists:
            return {'success': False, 'error': 'Destination account does not exist', 'code': 'INVALID_DESTINATION'}
        transaction_id = generate_transaction_id()
        processing_fee = calculate_processing_fee(transaction['amount'], transaction['currency'])
        return {'success': True, 'transaction_id': transaction_id, 'amount_processed': transaction['amount'], 'processing_fee': processing_fee, 'from_account': transaction['from_account'], 'to_account': transaction['to_account'], 'currency': transaction['currency'], 'timestamp': ml_datetime.now()}
    def get_account_balance(account_id):
        if (account_id == 'ACC001'):
            return {'balance': 25000, 'error': None}
        if (account_id == 'ACC002'):
            return {'balance': 5000, 'error': None}
        if (account_id == 'ACC003'):
            return {'balance': 100000, 'error': None}
        if (account_id == 'INVALID'):
            return {'balance': 0, 'error': 'Account not found'}
        return {'balance': 10000, 'error': None}
    def verify_account_exists(account_id):
        return ((account_id != 'NONEXISTENT') and (ml_string.length(account_id) >= 6))
    def generate_transaction_id():
        return (str('TXN') + str(ml_datetime.timestamp()))
    def calculate_processing_fee(amount, currency):
        base_fee = 2.5
        if (amount > 10000):
            base_fee = 5.0
        if (amount > 25000):
            base_fee = 10.0
        if (currency != 'USD'):
            base_fee = (base_fee * 1.2)
        return base_fee
    test_transactions = [{'amount': 1000, 'from_account': 'ACC001', 'to_account': 'ACC002', 'currency': 'USD', 'authorization_code': None}, {'amount': 75000, 'from_account': 'ACC003', 'to_account': 'ACC001', 'currency': 'USD', 'authorization_code': 'AUTH123456'}, {'amount': 500, 'from_account': 'ACC002', 'to_account': 'NONEXISTENT', 'currency': 'EUR', 'authorization_code': None}, {'amount': 30000, 'from_account': 'ACC001', 'to_account': 'ACC003', 'currency': 'USD', 'authorization_code': None}, {'amount': 100, 'from_account': 'ACC001', 'to_account': 'ACC002', 'currency': 'USD', 'authorization_code': None}, None]
    print('Financial transaction processing results:')
    l = 0
    while (l < test_transactions['length']()):
        transaction = test_transactions[l]
        result = process_financial_transaction(transaction)
        if result['success']:
            print((str((str((str((str((str('Transaction ') + str((l + 1)))) + str(': SUCCESS - ID: '))) + str(result['transaction_id']))) + str(', Fee: $'))) + str(result['processing_fee'])))
        else:
            print((str((str((str((str((str((str('Transaction ') + str((l + 1)))) + str(': FAILED - '))) + str(result['error']))) + str(' (Code: '))) + str(result['code']))) + str(')')))
        l = (l + 1)
    return test_transactions

def main():
    print('================================================')
    print('  COMPLEX CONTROL FLOW PATTERNS TEST')
    print('================================================')
    results = {}
    results['nested_conditions'] = complex_nested_conditions()
    results['advanced_loops'] = advanced_loop_patterns()
    results['switch_patterns'] = complex_switch_patterns()
    results['conditional_expressions'] = complex_conditional_expressions()
    results['guard_clauses'] = advanced_guard_clauses()
    print('\\n================================================')
    print('  ALL COMPLEX CONTROL FLOW TESTS COMPLETED')
    print('================================================')
    return results

main()

# End of generated code