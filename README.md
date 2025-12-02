# Databricks Apps Vibe Code Quickstart Guide 🚀

Get your Databricks-powered streamlit app up and running in 3 simple steps.

You will need to update following two things in step 1 and 2:

Databricks Host
Warehouse ID


---
## Prerequisites
1. Workspace must have SQL serverless compute active for use.
2. Sample data must be available to users. This example uses the "samples" catalog for reference.

---

## Step 1: Set Up Your Development Environment 🛠️

In your AI Tool run the following prompt:
```
Setup my local environment utilizing @instructions/01-setup-local_env.md as reference.
My Databricks Host is : 'https://e2-demo-field-eng.cloud.databricks.com/'
```

Fill in your databricks host name.
---

## Step 2: Build Your App 🏗️

In your AI Tool run the following prompt:
```
Write me an application utilizing @instructions/02-build-app.md

The warehouse id is :30d6e63b35f828c5

Then initiate the application for me.
```


---

## Step 3: Deploy with Databricks Asset Bundle 📦

In your AI Tool run the following prompt:
```
Create a Databricks Asset Bundle configuration utilizing @instructions/03-databricks-asset-bundle.md as reference.

Deploy the application using Databricks Asset Bundles.
```

This will:
- Generate the necessary `databricks.yml` configuration file
- Set up resource definitions for your app
- Configure deployment targets (dev/prod environments)
- Deploy your app to Databricks workspace

---

## Step 4: Be Creative 🎉

Extract a clean setup_env.zip to a new folder.

Update the 02-base-app.md to something like the following:
```
You are an app developer.
You are familiar with Databricks Unity Catalog and the 3 part naming structure.


Make me a X app based on these tables in Unity Catalog


Utilize the following: Apps cookbook reference 

```

You can utilize Faker to generate fake data if you need it to.
Feel free to switch it to plotly dash or other types of frameworks. Use the Apps cookbook as as a reference.

https://apps-cookbook.dev/

Rerun steps 1, 2 and 3 for your new app.




## 🆘 Need Help?

- **Environment issues?** Check the troubleshooting section in `01-setup-local_env.md`
- **Test your Databricks connection:** Run `python test_workspace_client.py`
- **Check dependencies:** Run `uv pip list` to see installed packages

---

## 📚 Additional Resources

- [Databricks SDK Documentation](https://docs.databricks.com/dev-tools/sdk-python.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [UV Package Manager](https://github.com/astral-sh/uv)
- [Apps Cookbook](https://apps-cookbook.dev/)

---

**Happy Building! 🎨✨**
