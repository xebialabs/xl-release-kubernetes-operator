package com.xebialabs.deployit.integration.test;

import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.junit.internal.runners.model.EachTestNotifier;
import org.junit.runner.Runner;
import org.junit.runner.notification.RunNotifier;
import org.junit.runners.BlockJUnit4ClassRunner;
import org.junit.runners.Parameterized;
import org.junit.runners.Suite;
import org.junit.runners.model.FrameworkMethod;
import org.junit.runners.model.InitializationError;
import org.junit.runners.model.Statement;
import org.junit.runners.model.TestClass;

/**
 */
public class NiceParameterizedNames extends Suite {
    private class TestClassRunnerForParameters extends BlockJUnit4ClassRunner {
        private final int fParameterSetNumber;

        private final List<Object[]> fParameterList;

        TestClassRunnerForParameters(Class<?> type, List<Object[]> parameterList, int i) throws InitializationError {
            super(type);
            fParameterList = parameterList;
            fParameterSetNumber = i;
        }

        @Override
        protected void runChild(FrameworkMethod method, RunNotifier notifier) {
            EachTestNotifier eachNotifier= new EachTestNotifier(notifier, describeChild(method));
            if (!(Boolean) computeParams()[1]) {
                eachNotifier.fireTestIgnored();
            } else {
                super.runChild(method, notifier);
            }
        }

        @Override
        public Object createTest() throws Exception {
            return getTestClass().getOnlyConstructor().newInstance(computeParams()[0]);
        }

        private Object[] computeParams() {
            try {
                return fParameterList.get(fParameterSetNumber);
            } catch (ClassCastException e) {
                throw new RuntimeException(String.format("%s.%s() must return a Collection of arrays.", getTestClass().getName(), getParametersMethod(getTestClass()).getName()));
            }
        }

        @Override
        protected String getName() {
            return String.format("[%s]", fParameterList.get(fParameterSetNumber)[0]);
        }

        @Override
        protected String testName(final FrameworkMethod method) {
            return String.format("%s%s", method.getName(), getName());
        }

        @Override
        protected void validateConstructor(List<Throwable> errors) {
            validateOnlyOneConstructor(errors);
        }

        @Override
        protected Statement classBlock(RunNotifier notifier) {
            return childrenInvoker(notifier);
        }
    }

    private final ArrayList<Runner> runners = new ArrayList<>();

    /**
     * Only called reflectively. Do not use programmatically.
     */
    public NiceParameterizedNames(Class<?> klass) throws Throwable {
        super(klass, Collections.emptyList());
        List<Object[]> parametersList = getParametersList(getTestClass());
        for (int i = 0; i < parametersList.size(); i++)
            runners.add(new TestClassRunnerForParameters(getTestClass().getJavaClass(), parametersList, i));
    }

    @Override
    protected List<Runner> getChildren() {
        return runners;
    }

    @SuppressWarnings("unchecked")
    private static List<Object[]> getParametersList(TestClass klass) throws Throwable {
        return (List<Object[]>) getParametersMethod(klass).invokeExplosively(null);
    }

    private static FrameworkMethod getParametersMethod(TestClass testClass) {
        List<FrameworkMethod> methods = testClass.getAnnotatedMethods(Parameterized.Parameters.class);
        for (FrameworkMethod each : methods) {
            int modifiers = each.getMethod().getModifiers();
            if (Modifier.isStatic(modifiers) && Modifier.isPublic(modifiers))
                return each;
        }

        throw new RuntimeException("No public static parameters method on class " + testClass.getName());
    }

}
